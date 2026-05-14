from fastapi import APIRouter, Depends, HTTPException, status
from ..models.database.session import get_session
from ..models.repositories.user_repository import UserRepository
from ..models.repositories.student_repository import StudentRepository
from ..schemas.user_schema import UserLoginSchema
from .jwt import create_access_token

login_router = APIRouter(prefix="/auth", tags=["auth"])


@login_router.post("/login")
async def login(data: UserLoginSchema, session=Depends(get_session)):

    # 1. Tenta encontrar em users (admin, coach)
    user_repo = UserRepository(session)
    user = user_repo.get_by_email(data.email)

    if user:
        if not user_repo.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou password incorrectos."
            )
        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta inactiva."
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
                "ativo": user.ativo,
            }
        }

    # 2. Tenta encontrar em students
    student_repo = StudentRepository(session)
    student = student_repo.get_by_email(data.email)

    if student:
        if not student_repo.verify_password(data.password, student.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou password incorrectos."
            )
        if not student.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta ainda não activada. Verifica o teu email."
            )
        token = create_access_token({"sub": student.id, "role": "student"})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": student.id,
                "nome": student.nome,
                "email": student.email,
                "role": "student",
                "ativo": student.ativo,
            }
        }

    # 3. Não encontrado em nenhuma tabela
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou password incorrectos."
    )