from fastapi import APIRouter, Depends, HTTPException, status
from ..models.database.session import get_session
from ..models.repositories.user_repository import UserRepository
from ..schemas.user_schema import UserLoginSchema
from .jwt import create_access_token

login_router = APIRouter(prefix="/auth", tags=["auth"])


@login_router.post("/login")
async def login(data: UserLoginSchema, session=Depends(get_session)):
    repo = UserRepository(session)
    user = repo.get_by_email(data.email)

    if not user or not repo.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou password incorrectos."
        )

    token = create_access_token({"sub": user.id, "role": user.role})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "role": user.role,
            "ativo": user.ativo
        }
    }