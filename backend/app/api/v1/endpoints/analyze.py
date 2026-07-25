import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.document_parser import parse_document
from app.core.state import session_store
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB

from app.services.ollama_provider import OllamaProvider
from app.services.gemini_provider import GeminiProvider

def get_provider(provider_name: str):
    if provider_name == "gemini":
        return GeminiProvider()
    return OllamaProvider()

@router.post("")
async def analyze_document(
    file: UploadFile = File(...),
    language: str = Form("English"),
    provider: str = Form("gemma-local")
):
    # 1. Validate file size (approximation by checking content length if available, or reading chunks)
    # Read the file to memory (we need it for parsing anyway)
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
        
    await file.seek(0)
    
    # 2. Extract text
    try:
        extracted_text = await parse_document(file)
    except Exception as e:
        logger.error(f"Failed to parse document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the document.")

    # 3. Construct prompt
    prompt = f"""
    You are CivicAI, a helpful public service assistant. A user has uploaded an official document.
    Analyze the following extracted text from the document.
    
    Document Text:
    ---
    {extracted_text}
    ---
    
    Perform the following tasks:
    1. Explain what this document is and what it says in plain language.
    2. Assess the user's eligibility for whatever scheme or action is mentioned.
    3. Provide a step-by-step checklist of actions the user needs to take (with deadlines if applicable).
    4. Detect any missing documents that the user still needs to provide.
    
    IMPORTANT: You must translate the ENTIRE response (explanation, eligibility text, checklist items, missing documents) into {language}.
    """
    
    # Instantiate provider
    ai_service = get_provider(provider)

    # 4. Call Provider
    try:
        result = await ai_service.generate_json(prompt)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"JSON generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze document with AI.")
        
    # 5. Create session
    session_id = str(uuid.uuid4())
    session_store[session_id] = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": str(result)} # store the raw stringified JSON for context
    ]
    
    # 6. Return exact expected schema + session_id
    result["session_id"] = session_id
    
    return result
