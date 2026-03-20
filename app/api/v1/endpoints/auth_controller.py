from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel,EmailStr,Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.candidate import CreateUserRequest,LoginUserRequest,RefreshToken,VerifyToken,ForgetPassword,ResetPassword,UpdatePassword
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
    

@router.post("/verify")
async def verify_token(request:VerifyToken,session:AsyncSession= Depends(get_db)):
    
    try:
        email = await LoginService.verify_token(request.token)
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        
        data_service = DataService(session)
        candidate = data_service.verify_candidate(email)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Candidate Not Found.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Verify Successfully. Thank You!"
        )
    
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))
    


@router.post("/forget_password")
async def forget_password(request:ForgetPassword,session:AsyncSession= Depends(get_db)):
    try:
       
        data_service = DataService(session)
        candidate = await data_service.candidate_by_email(request.email)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Candidate Not Found.")
        
        referese_token = await LoginService.create_refresh_token(candidate.email)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "rest_password":f"https://hitchier-duane-ingenuously.ngrok-free.dev?refrese_token={referese_token}",
                "token":referese_token
                }
        )
        
                
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    

@router.post("/reset_password")
async def reset_password(request:ResetPassword,session:AsyncSession=Depends(get_db)):
    
    try:
        email = await LoginService.verify_token(request.token)
        
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        
        data_service= DataService(session)
        candidate = await data_service.reset_password(email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=candidate
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
@router.post("/update_password")
async def update_password(request:UpdatePassword,session:AsyncSession = Depends(get_db)):
    
    try:
        
        email = await LoginService.verify_token(request.token)
        
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        data_service= DataService(session)
        
        candidate = await data_service.update_password(email,request.new_password,request.verfiy_password)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Password updated successfully"}
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))