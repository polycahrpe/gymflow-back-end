from .base_schema import BaseModel, Optional, field_validator
from datetime import date
from enum import Enum


class PaymentStatusSchema(str, Enum):
    pago = "pago"
    pendente = "pendente"
    atrasado = "atrasado"


class PaymentBaseSchema(BaseModel):
    student_id: str
    payment_plan_id: str
    valor: float
    data_pagamento: date
    observacao: Optional[str] = None

    @field_validator("valor")
    def validate_valor(cls, valor):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return valor


class PaymentCreateSchema(PaymentBaseSchema):
    pass


class PaymentUpdateSchema(BaseModel):
    valor: Optional[float] = None
    data_pagamento: Optional[date] = None
    status: Optional[PaymentStatusSchema] = None
    observacao: Optional[str] = None

    @field_validator("valor")
    def validate_valor(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return valor


class StudentInfoSchema(BaseModel):
    id: str
    nome: str
    email: str
    genero: str
    ativo: bool

    class Config:
        from_attributes = True


class PaymentPlanInfoSchema(BaseModel):
    id: str
    nome: str
    preco: float
    duracao_dias: int

    class Config:
        from_attributes = True


class PaymentResponseSchema(BaseModel):
    id: str
    student_id: str
    payment_plan_id: str
    valor: float
    data_pagamento: date
    data_vencimento: date
    status: PaymentStatusSchema
    observacao: Optional[str] = None
    student: Optional[StudentInfoSchema] = None
    payment_plan: Optional[PaymentPlanInfoSchema] = None

    class Config:
        from_attributes = True