from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel,EmailStr,Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.candidate import CreateUserRequest,LoginUserRequest,RefreshToken
from app.services.data_services import DataService
from app.services.login_services import LoginService

router = APIRouter(prefix="/candidate", tags=["Candidate"])


@router.post("/create")
async def create_candidate(request:CreateUserRequest, session:AsyncSession = Depends(get_db)):
    try:
        data_service = DataService(session)
        candidate = await data_service.create_candidate(request.email)
        print("New password----------------",candidate["password"])
        
        return {"email": candidate["email"], "id": candidate["id"]}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    

@router.post("/login")
async def login(request:LoginUserRequest,session:AsyncSession = Depends(get_db)):
    
    try:
        response = await LoginService.login_with_email_password(email=request.email,password=request.password,session=session)
        return response
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@router.post("/refresh_token")
async def refresh_token(request:RefreshToken,session:AsyncSession = Depends(get_db)):
    
    try:
        response = await LoginService.refresh_token(request.token,session)
        return response
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(exc))