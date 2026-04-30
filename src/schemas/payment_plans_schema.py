from .base_schema import (
    BaseModel, uuid4, UUID, Field, List,
    Optional, field_validator, re
)


class StudentSummarySchema(BaseModel):
    id: str
    nome: str
    email: str
    ativo: bool

    class Config:
        from_attributes = True


class PaymentPlansBaseSchema(BaseModel):
    nome: str
    preco: float
    duracao_dias: int
    exercicios: list[str]

    @field_validator("nome")
    def validate_name(cls, name):
        name = name.strip()
        if len(name) < 5:
            raise ValueError("O nome deve ter no mínimo 5 caracteres.")
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", name):
            raise ValueError("O nome não deve conter números nem caracteres especiais.")
        return name

    @field_validator("preco")
    def validate_price(cls, price):
        if price <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        return price


class PaymentPlansCreateSchema(PaymentPlansBaseSchema):
    pass


class PaymentPlansUpdateSchema(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    duracao_dias: Optional[int] = None
    exercicios: Optional[list[str]] = None


class PaymentPlansResponseSchema(BaseModel):
    id: str
    nome: str
    preco: float
    duracao_dias: int
    ativo: bool
    exercicios: list[str]
    students: list[StudentSummarySchema] = []  # ← novo

    @field_validator("exercicios", mode="before")
    @classmethod
    def parse_exercicios(cls, value):
        return [
            e.nome if hasattr(e, "nome") else e
            for e in value
        ]

    class Config:
        from_attributes = True


class PaymentPlansGetSchema(BaseModel):
    id: str
    nome: str
    preco: float
    duracao_dias: int
    ativo: bool
    exercicios: list[str]
    students: list[StudentSummarySchema] = []  # ← novo

    @field_validator("exercicios", mode="before")
    @classmethod
    def parse_exercicios(cls, value):
        return [
            e.nome if hasattr(e, "nome") else e
            for e in value
        ]

    class Config:
        from_attributes = True