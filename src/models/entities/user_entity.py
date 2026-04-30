from .base_entity import ( String, Boolean, Enum, uuid4, enum, mapped_column )
from ..database.config import Base
from sqlalchemy.orm import Mapped


class UserRole(str, enum.Enum):
    admin = "admin"
    coach = "coach"
    client = "client"


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.client)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)