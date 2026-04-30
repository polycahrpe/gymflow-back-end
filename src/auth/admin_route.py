from fastapi import APIRouter, Depends
from ..models.database.session import get_session
from ..models.repositories.user_repository import UserRepository
from ..schemas.user_schema import UserCreateSchema, UserResponseSchema, UserRole
from .dependencies import require_role

admin_router = APIRouter(prefix="/auth", tags=["auth"])


@admin_router.post("/register-admin", response_model=UserResponseSchema)
async def register_admin(
    data: UserCreateSchema,
    session=Depends(get_session),
    _=Depends(require_role("admin"))  # só admins podem criar outros admins
):
    data.role = UserRole.admin
    repo = UserRepository(session)
    return repo.create(data)