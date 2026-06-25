from .base_schema import BaseModel, Optional, List, field_validator
from datetime import datetime
from enum import Enum


class DiaSemanaSchema(str, Enum):
    segunda = "segunda"
    terca = "terca"
    quarta = "quarta"
    quinta = "quinta"
    sexta = "sexta"
    sabado = "sabado"
    domingo = "domingo"


# ─────────────────────────────────────────
# EXERCÍCIO
# ─────────────────────────────────────────
class WorkoutExerciseSchema(BaseModel):
    dia_semana: DiaSemanaSchema
    nome: str
    series: int
    repeticoes: int
    carga: Optional[float] = None

    @field_validator("series", "repeticoes")
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return v


class WorkoutExerciseResponseSchema(BaseModel):
    id: str
    dia_semana: DiaSemanaSchema
    nome: str
    series: int
    repeticoes: int
    carga: Optional[float] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# FICHA DE TREINO
# ─────────────────────────────────────────
class WorkoutPlanCreateSchema(BaseModel):
    student_id: str
    titulo: str
    exercicios: List[WorkoutExerciseSchema]

    @field_validator("titulo")
    def validate_titulo(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("O título deve ter pelo menos 3 caracteres.")
        return v

    @field_validator("exercicios")
    def validate_exercicios(cls, v):
        if len(v) == 0:
            raise ValueError("A ficha deve ter pelo menos um exercício.")
        return v


class WorkoutPlanUpdateSchema(BaseModel):
    titulo: Optional[str] = None
    ativo: Optional[bool] = None
    exercicios: Optional[List[WorkoutExerciseSchema]] = None


class WorkoutPlanResponseSchema(BaseModel):
    id: str
    student_id: str
    coach_id: str
    titulo: str
    data_criacao: datetime
    ativo: bool
    exercicios: List[WorkoutExerciseResponseSchema] = []

    class Config:
        from_attributes = True