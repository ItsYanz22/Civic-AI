from typing import Dict, List, Any

# In-memory store for session histories.
# Format: { "uuid": [ {"role": "user"|"assistant", "content": "..."} ] }
session_store: Dict[str, List[Dict[str, str]]] = {}
