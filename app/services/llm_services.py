
from app.core.config import settings
from typing import Optional,List,Dict,Any
import httpx
from fastapi import HTTPException

class LLMService:
    
    def __init__(self):
        self.api_key = settings.ALBIO_API_KEY #os.getenv("CYANAI_API_KEY", "")
        self.base_url = settings.ALBIO_API_BASE_URL #os.getenv("CYANAI_API_BASE_URL", "")
        
        if not self.api_key:
            raise ValueError("ALBIO_API_KEY environment variable is required")
    
    async def invoke_agent(
        self,
        agent_name:str,
        messages:Optional[List[dict]] = None,
        response_format: Optional[Any] = None,
        custom_api_key: Optional[str] = None,
        prompt_type: str = ""
        
    ):
        try:
            # api_key = custom_api_key or self.api_key
            payload = {
                "agentName": agent_name,
                "messages": messages,
                "response_format": response_format
            }
            print("--before-------------result")   
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/agentic/invoke",
                    json=payload,
                    headers={
                        # "X-API-Key": self.api_key,
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=60.0
                )
                if response.status_code == 200:
                    response_data = response.json()
                    return response_data
                else:
                    error_detail = response.text
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"AlbioAI service error: {error_detail}"
                    )
        except httpx.TimeoutException:
            raise HTTPException(status_code=408, detail="Request to AlbioAI service timed out")
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error connecting to AlbioAI service: {str(e)}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
            
            


def get_llm_service():
    try:
        return LLMService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))