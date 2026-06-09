from .base_schema import BaseModel, Optional
from datetime import date, time, datetime
from enum import Enum


class AttendanceStatusSchema(str, Enum):
    pendente_entrada = "pendente_entrada"
    presente         = "presente"
    pendente_saida   = "pendente_saida"
    saiu             = "saiu"


class AttendanceMarkEntrySchema(BaseModel):
    student_id: str
    data: date
    hora_entrada: time


class AttendanceMarkExitSchema(BaseModel):
    student_id: str
    hora_saida: time


class StudentAttendanceSummarySchema(BaseModel):
    id: str
    nome: str
    email: str
    genero: str
    ativo: bool

    class Config:
        from_attributes = True


class AttendanceResponseSchema(BaseModel):
    id: str
    student_id: str
    data: date
    hora_entrada: Optional[time] = None
    hora_saida: Optional[time] = None
    status: AttendanceStatusSchema
    confirmado_entrada_em: Optional[datetime] = None
    confirmado_saida_em: Optional[datetime] = None
    student: Optional[StudentAttendanceSummarySchema] = None

    class Config:
        from_attributes = True