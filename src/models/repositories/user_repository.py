from .base_repository import HTTPException, status, Session
from ..entities.user_entity import UserEntity
from ...schemas.user_schema import UserCreateSchema
import bcrypt


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.query(UserEntity).filter(UserEntity.email == email).first()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def create(self, data: UserCreateSchema) -> UserEntity:
        existing = self.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um utilizador com este email."
            )

        user = UserEntity(
            nome=data.nome,
            email=data.email,
            password=self.hash_password(data.password),
            role=data.role
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user