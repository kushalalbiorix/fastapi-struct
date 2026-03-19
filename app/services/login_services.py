import os
import jwt
import json
import bcrypt
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from app.core.config import settings
from app.services.data_services import DataService
from app.db.session import get_db,AsyncSessionLocal



class LoginService:
    
    @staticmethod
    async def _create_token(email:str,expires_delta:timedelta,token_type:str,extra_claims:dict | None = None):
        
        expire = datetime.utcnow() + expires_delta
        payload = {"sub": email, "type": token_type, "exp": expire}
        if token_type == "refresh":
            payload["jti"] = str(uuid4())
        if extra_claims:
            payload.update(extra_claims)
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    @staticmethod
    async def _decode_token(token:str,expected_type:str | None = None):
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            if expected_type and payload.get("type") != expected_type:
                raise ValueError("Invalid token type.")
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")

    
    @staticmethod
    async def create_access_token(email:str):
        
        return await LoginService._create_token(
            email,
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "access"
        )
    
    @staticmethod
    async def create_refresh_token(email:str):
        return await LoginService._create_token(
            email,
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "refresh"
        )
    
    @staticmethod
    async def create_login_tokens(email:str):
        return {
            "access_token":await LoginService.create_access_token(email),
            "refresh_token":await LoginService.create_refresh_token(email)
        }
        
    
    @staticmethod
    async def login_with_email_password(email:str,password:str,session = None):
        
        data_service = DataService(session)
        
        candidate = await data_service.candidate_by_email(email=email)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is No any candidate using {email} email.")
        
        if not bcrypt.checkpw(password.encode(),candidate.password.encode()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        candidate.verified = True
        data_service.session.add(candidate)
        await data_service.session.commit()
        return await LoginService.create_login_tokens(email=email)
    
    
    
    
    
    @staticmethod 
    async def get_current_candidate(credentials:HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        
        token =credentials.credentials
        try:
            payload = await LoginService._decode_token(token=token)
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Invalid Token")
            
            async with AsyncSessionLocal() as session:
                data_service = DataService(session)
                candidate = await data_service.candidate_by_email(email=email)
                if not candidate:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Candidate Not found")
            
            return candidate
            
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(exc))
        
    
    @staticmethod
    async def refresh_token(refresh_token:str, session = None):
        
        payload = await LoginService._decode_token(token=refresh_token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
        
        if not session:
            async with AsyncSessionLocal as session:
                data_service = DataService(session)
                candidate = await data_service.candidate_by_email(email=email)
        else:
            data_service = DataService(session)
            candidate = await data_service.candidate_by_email(email=email)
            
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Candidate Not found")
            
        return await LoginService.create_login_tokens(email=email)
        
        
    