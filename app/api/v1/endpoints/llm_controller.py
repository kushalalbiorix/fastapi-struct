from fastapi import APIRouter,Depends,HTTPException,status
from app.core.config import settings
from app.schemas.llms import ProxyInvokeRequest
from app.services.llm_services import LLMService,get_llm_service
from app.services.login_services import LoginService
from app.models.candidate import Candidate
from fastapi.responses import JSONResponse

router = APIRouter()




@router.post("/invoke")
async def invoke_albai(
    request:ProxyInvokeRequest,
    llm_service:LLMService = Depends(get_llm_service),
    current_candidate: Candidate = Depends(LoginService.get_current_candidate)
    
):
    try:
        result = await llm_service.invoke_agent(
            agent_name=request.agentName,
            messages=request.messages,
            response_format=request.response_format,
            custom_api_key=request.api_key,
            prompt_type=request.promptType
        )
        print(result,"---------------result")
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
