from ..database.config import Base
from .base_entity import String, uuid4, Mapped, mapped_column, Boolean


class AccessCodeEntity(Base):
    __tablename__ = "access_codes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    code: Mapped[str] = mapped_column(String(5), unique=True, nullable=False)
    usado: Mapped[bool] = mapped_column(Boolean, default=False)