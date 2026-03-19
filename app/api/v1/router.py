from fastapi import APIRouter
 
from app.api.v1.endpoints import  users,auth_controller,llm_controller
 
api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth_controller.router)
api_router.include_router(llm_controller.router)