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
    access_code: str

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

    @field_validator("access_code")
    def validate_access_code(cls, v):
        if not v.isdigit() or len(v) != 5:
            raise ValueError("O código de acesso deve ter exactamente 5 dígitos.")
        return v


class StudentUpdateSchema(BaseModel):
    nome: Optional[str] = None
    genero: Optional[StudentGenero] = None
    coach_id: Optional[str] = None
    payment_plan_id: Optional[str] = None


class CoachSummarySchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    especialidade: str
    genero: str
    ativo: bool

    class Config:
        from_attributes = True


class PaymentPlanSummarySchema(BaseModel):
    id: str
    nome: str
    preco: float
    duracao_dias: int
    ativo: bool

    class Config:
        from_attributes = True


class StudentResponseSchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    genero: StudentGenero
    ativo: bool
    coach_id: str
    payment_plan_id: str
    coach: Optional[CoachSummarySchema] = None
    payment_plan: Optional[PaymentPlanSummarySchema] = None

    class Config:
        from_attributes = True


class StudentSummarySchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    genero: StudentGenero
    ativo: bool

    class Config:
        from_attributes = True