
from pydantic import BaseModel
from typing import Optional, List, Any

class ProxyInvokeRequest(BaseModel):
    messages: Optional[List[dict]] = None
    agentName: str
    response_format: Optional[Any] = None
    api_key: Optional[str] = None
    promptType: Optional[str] = ""