from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.core.state import session_store
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

from app.services.ollama_provider import OllamaProvider
from app.services.gemini_provider import GeminiProvider
from app.services.snowflake_service import log_chat_message

def get_provider(provider_name: str):
    if provider_name == "gemini":
        return GeminiProvider()
    return OllamaProvider()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    provider: str = "gemma-local"

class ChatResponse(BaseModel):
    reply: str

@router.post("")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    session_id = request.session_id
    
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found or expired.")
        
    history = session_store[session_id]
    ai_service = get_provider(request.provider)
    
    try:
        # Call provider chat
        reply = await ai_service.chat(history, request.message)
        
        # Update history
        history.append({"role": "user", "content": request.message})
        history.append({"role": "assistant", "content": reply})
        
        # Snowflake Integration: Log the chat exchange
        background_tasks.add_task(log_chat_message, session_id, "user", request.message)
        background_tasks.add_task(log_chat_message, session_id, "assistant", reply)
        
        return {"reply": reply}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate chat response.")
