from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    @abstractmethod
    async def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Generates a JSON response matching the AnalyzeResponseSchema.
        """
        pass

    @abstractmethod
    async def chat(self, history: List[Dict[str, str]], new_message: str) -> str:
        """
        Processes a chat message given context history.
        """
        pass
