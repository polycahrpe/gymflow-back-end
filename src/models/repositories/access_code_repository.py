from .base_repository import HTTPException, status, Session
from ..entities.access_code_entity import AccessCodeEntity
import random
import string


def _generate_code() -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=7))


class AccessCodeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(AccessCodeEntity).all()

    def generate(self) -> AccessCodeEntity:
        for _ in range(10):
            code = _generate_code()
            existing = self.session.query(AccessCodeEntity).filter(
                AccessCodeEntity.code == code,
                AccessCodeEntity.usado == False
            ).first()
            if not existing:
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Não foi possível gerar um código único. Tenta novamente."
            )

        access_code = AccessCodeEntity(code=code)
        self.session.add(access_code)
        self.session.commit()
        self.session.refresh(access_code)
        return access_code

    def validate_and_consume(self, code: str) -> bool:
        access_code = self.session.query(AccessCodeEntity).filter(
            AccessCodeEntity.code == code.upper(),
            AccessCodeEntity.usado == False
        ).first()

        if not access_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de acesso inválido ou já utilizado."
            )

        access_code.usado = True
        self.session.commit()
        return True