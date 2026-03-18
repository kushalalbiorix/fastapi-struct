import uuid

from fastapi import APIRouter, status



router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def info():
    return {"API":"Well Come"}