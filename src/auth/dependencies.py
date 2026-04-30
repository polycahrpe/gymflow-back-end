from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt import verify_token
from ..models.database.session import get_session
from ..models.entities.user_entity import UserEntity

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session=Depends(get_session)
) -> UserEntity:
    payload = verify_token(credentials.credentials)
    user = session.query(UserEntity).filter(UserEntity.id == payload.get("sub")).first()

    if not user or not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador não encontrado ou inactivo."
        )
    return user


def require_role(*roles: str):
    def dependency(current_user: UserEntity = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para aceder a este recurso."
            )
        return current_user
    return dependency