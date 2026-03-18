




import uuid
from typing import Optional

from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.repo.get_by_email(email)

    async def list_users(self, *, page: int = 1, size: int = 20):
        skip = (page - 1) * size
        items, total = await self.repo.list(skip=skip, limit=size)
        pages = (total + size - 1) // size
        return {"items": items, "total": total, "page": page, "size": size, "pages": pages}

    async def create(self, data: UserCreate) -> User:
        if await self.repo.exists_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )
        return await self.repo.create(
            {
                "email": data.email,
                "full_name": data.full_name,
                "hashed_password": hash_password(data.password),
                "is_active": data.is_active,
                "is_superuser": data.is_superuser,
            }
        )

    async def update(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        updates = data.model_dump(exclude_unset=True)
        if "password" in updates:
            updates["hashed_password"] = hash_password(updates.pop("password"))
        return await self.repo.update(user, updates)

    async def delete(self, user_id: uuid.UUID) -> None:
        user = await self.get_by_id(user_id)
        await self.repo.delete(user)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user