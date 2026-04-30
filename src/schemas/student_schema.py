from .base_schema import BaseModel, EmailStr, Optional, Enum, field_validator, re


class StudentGenero(str, Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"


class StudentCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    password: str
    genero: StudentGenero
    coach_id: str
    payment_plan_id: str

    @field_validator("nome")
    def validate_nome(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres.")
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", v):
            raise ValueError("O nome não deve conter números nem caracteres especiais.")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v.strip()) < 6:
            raise ValueError("Password deve ter pelo menos 6 caracteres.")
        return v


class StudentResponseSchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    genero: StudentGenero
    ativo: bool
    coach_id: str
    payment_plan_id: str

    class Config:
        from_attributes = True