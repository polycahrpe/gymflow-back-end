from .base_schema import BaseModel, EmailStr, Optional, Enum, field_validator, re
from .student_schema import StudentSummarySchema  # 👈


class CoachEspecialidade(str, Enum):
    musculacao = "musculacao"
    crossfit = "crossfit"
    yoga = "yoga"
    pilates = "pilates"
    natacao = "natacao"
    funcional = "funcional"


class CoachGenero(str, Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"


class CoachCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    password: str
    especialidade: CoachEspecialidade
    genero: CoachGenero

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


class CoachResponseSchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    especialidade: CoachEspecialidade
    genero: CoachGenero
    ativo: bool
    students: list[StudentSummarySchema] = []  # 👈 alunos sem coach dentro

    class Config:
        from_attributes = True