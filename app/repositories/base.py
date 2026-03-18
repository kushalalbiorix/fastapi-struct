from typing import Any, Generic, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """
    Generic async CRUD repository.
    Inherit and set `model` on the subclass.
    """

    model: Type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: UUID) -> Optional[ModelT]:
        return await self.session.get(self.model, id)

    async def get_or_raise(self, id: UUID) -> ModelT:
        obj = await self.get(id)
        if obj is None:
            raise ValueError(f"{self.model.__name__} with id={id} not found")
        return obj

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[dict[str, Any]] = None,
    ) -> tuple[Sequence[ModelT], int]:
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        if filters:
            for field, value in filters.items():
                if value is not None:
                    col = getattr(self.model, field)
                    query = query.where(col == value)
                    count_query = count_query.where(col == value)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        result = await self.session.execute(query.offset(skip).limit(limit))
        items = result.scalars().all()

        return items, total

    async def create(self, obj_in: dict[str, Any]) -> ModelT:
        obj = self.model(**obj_in)
        self.session.add(obj)
        await self.session.flush()  # Flush to get DB-generated values (e.g. id)
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelT, updates: dict[str, Any]) -> ModelT:
        for field, value in updates.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self.session.delete(obj)
        await self.session.flush()