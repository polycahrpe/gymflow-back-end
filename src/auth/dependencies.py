from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt import verify_token
from ..models.database.session import get_session
from ..models.entities.user_entity import UserEntity
from ..models.entities.student_entity import StudentEntity

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session=Depends(get_session)
):
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    role = payload.get("role")

    # Se o role for student, busca na tabela students
    if role == "student":
        user = session.query(StudentEntity).filter(StudentEntity.id == user_id).first()
    else:
        user = session.query(UserEntity).filter(UserEntity.id == user_id).first()

    if not user or not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador não encontrado ou inactivo."
        )
    return user


def require_role(*roles: str):
    def dependency(current_user=Depends(get_current_user)):
        role = getattr(current_user, "role", "student") if not hasattr(current_user, "role") else current_user.role

        # StudentEntity não tem campo role, inferimos pelo tipo
        if isinstance(current_user, StudentEntity):
            current_role = "student"
        else:
            current_role = current_user.role

        if current_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para aceder a este recurso."
            )
        return current_user
    return dependency