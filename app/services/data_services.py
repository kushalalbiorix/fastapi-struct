
from sqlalchemy import select,delete
from sqlalchemy.orm import selectinload

from datetime import datetime,UTC,timedelta
import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from sqlalchemy import select
from app.models.candidate import Candidate
import bcrypt


class DataService:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    def _generate_humun_readble_password(self,length=6):
        import random

        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Exclude I, O, 1, 0
        return "".join(random.choices(chars, k=length))

        
    async def candidate_by_email(self, email:str):
        
        result = await self.session.execute(
            select(Candidate).where(Candidate.email == email)
        )
       
        return result.scalar_one_or_none()        
        
    async def create_candidate(self,email:str):
        
        existing = await self.candidate_by_email(email=email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="candidate with this email already exists.")
      
        password = self._generate_humun_readble_password()
        hashed_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        
        candidate = Candidate(
            id = uuid.uuid4(),
            email = email,
            status = "created",
            verified = False,
            password  = hashed_password,
            date_created = datetime.now(UTC),
            user_created = None,
            custom_password_set =False
            
        )
        self.session.add(candidate)
        await self.session.flush()
        
        
        return {"id":candidate.id, "email":candidate.email, "password":password}
    
    
    
    async def verify_candidate(self,email:str):
        
        candidate  = await self.candidate_by_email(email)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalide email")
        
        candidate.verified = True
        # self.session.add(candidate)
        await self.session.commit()
        return candidate
    
    async def reset_password(self,email:str):
        
        candidate = await self.candidate_by_email(email)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalide email")
        
        generate_password =  self._generate_humun_readble_password()
        
        decoded = bcrypt.hashpw(generate_password.encode(),bcrypt.gensalt()).decode()
        
        candidate.password = decoded
        # self.session.add(candidate)
        await self.session.commit()
        
        return {
            "email": candidate.email,
            "password":generate_password
        }
        
    
    async def update_password(self,email:str,new_password:str,verify_password:str):
        
        candidate = await self.candidate_by_email(email)
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalide email")
        decoded = bcrypt.hashpw(new_password.encode(),bcrypt.gensalt()).decode()
        
        candidate.password = decoded
        await self.session.commit()
        return {
            "email": candidate.email,
            "password":new_password
        }
        
    