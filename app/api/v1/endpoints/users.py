import uuid

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, Pagination, SuperUser, UserServiceDep
from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserListResponse, dependencies=[])
async def list_users(
    pagination: Pagination,
    user_service: UserServiceDep,
    _: SuperUser,  # Only superusers can list all users
):
    return await user_service.list_users(page=pagination.page, size=pagination.size)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate,
    user_service: UserServiceDep,
    _: SuperUser,
):
    return await user_service.create(body)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: CurrentUser):
    """Returns the authenticated user's own profile."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    user_service: UserServiceDep,
    _: SuperUser,
):
    return await user_service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    body: UserUpdate,
    user_service: UserServiceDep,
    current_user: CurrentUser,
):
    # Users can update themselves; superusers can update anyone
    if not current_user.is_superuser and current_user.id != user_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not enough permissions.")
    return await user_service.update(user_id, body)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    user_service: UserServiceDep,
    _: SuperUser,
):
    await user_service.delete(user_id)