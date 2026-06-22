from .base_schema import BaseModel, EmailStr, Optional, Enum, field_validator, re
from typing import List
from datetime import datetime


class CoachEspecialidade(str, Enum):
    musculacao = "musculacao"
    crossfit = "crossfit"
    yoga = "yoga"
    pilates = "pilates"
    natacao = "natacao"
    funcional = "funcional"


class CoachExperiencia(str, Enum):
    musculacao = "musculacao"
    crossfit = "crossfit"
    yoga = "yoga"
    pilates = "pilates"
    natacao = "natacao"
    funcional = "funcional"
    boxe = "boxe"
    artes_marciais = "artes_marciais"
    spinning = "spinning"
    zumba = "zumba"
    calistenia = "calistenia"
    alongamento = "alongamento"
    atletismo = "atletismo"
    nutricao_esportiva = "nutricao_esportiva"


class CoachGenero(str, Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"


class CoachCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    password: str
    especialidade: CoachEspecialidade
    experiencias: List[CoachExperiencia] = []
    genero: CoachGenero
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
        if len(v) != 7 or not v.isalnum():
            raise ValueError("O código de acesso deve ter exactamente 7 caracteres alfanuméricos.")
        return v.upper()


class CoachUpdateSchema(BaseModel):
    nome: Optional[str] = None
    especialidade: Optional[CoachEspecialidade] = None
    experiencias: Optional[List[CoachExperiencia]] = None
    genero: Optional[CoachGenero] = None


class CoachExperienciaResponseSchema(BaseModel):
    id: str
    nome: str

    class Config:
        from_attributes = True


class StudentSummaryForCoachSchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    genero: str
    ativo: bool
    dias_restantes: int
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None

    class Config:
        from_attributes = True


class CoachResponseSchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    especialidade: CoachEspecialidade
    experiencias: List[CoachExperienciaResponseSchema]
    genero: CoachGenero
    ativo: bool

    class Config:
        from_attributes = True


class CoachDetailResponseSchema(BaseModel):
    id: str
    nome: str
    email: EmailStr
    especialidade: CoachEspecialidade
    experiencias: List[CoachExperienciaResponseSchema]
    genero: CoachGenero
    ativo: bool
    students: List[StudentSummaryForCoachSchema] = []  # nome correcto da relação

    class Config:
        from_attributes = True