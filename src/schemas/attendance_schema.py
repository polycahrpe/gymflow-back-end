from .base_schema import BaseModel, Optional
from datetime import date, time, datetime
from enum import Enum


class AttendanceStatusSchema(str, Enum):
    pendente_entrada = "pendente_entrada"
    presente         = "presente"
    pendente_saida   = "pendente_saida"
    saiu             = "saiu"


# ─────────────────────────────────────────
# Resposta do QR code gerado (entrada ou saída)
# ─────────────────────────────────────────
class AttendanceQRSchema(BaseModel):
    attendance_id: str
    token: str
    token_expira_em: datetime
    status: AttendanceStatusSchema

    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# Resposta completa de uma presença
# ─────────────────────────────────────────
class AttendanceResponseSchema(BaseModel):
    id: str
    student_id: str
    token: str
    token_expira_em: datetime
    data: date
    hora_entrada: Optional[time] = None
    hora_saida: Optional[time] = None
    status: AttendanceStatusSchema
    confirmado_entrada_em: Optional[datetime] = None
    confirmado_saida_em: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# Payload que o admin envia para confirmar (token do QR)
# ─────────────────────────────────────────
class AttendanceConfirmSchema(BaseModel):
    token: str