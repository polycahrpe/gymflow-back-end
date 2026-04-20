from .main_entity import (Field, SQLModel, field_validator)


class PaymentPlan(SQLModel):
    name: str = Field(..., description="The name of the payment plan")
    price: float = Field(..., description="The price of the payment plan")
    duration_months: str = Field(..., description="The duration of the payment plan in months")
    description: str = Field(..., description="A description of the payment plan")

    @field_validator("name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("O nome do plano de pagamento não pode ser vazio.")
        
        if len(value) > 100:
            raise ValueError("O nome do plano de pagamento não pode exceder 100 caracteres.")
        
        return value
    

    @field_validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("O preço do plano de pagamento deve ser maior que zero.")

        if value > 100000:
            raise ValueError("O preço do plano de pagamento não pode exceder 10.000.")

        return value


    @field_validator("duration_months")
    def validate_duration_months(cls, value):
        if not value.strip():
            raise ValueError("A duração do plano de pagamento não pode ser vazia.")
        
        if value == "0":
            raise ValueError("A duração do plano de pagamento deve ser maior que zero.")    

        return value
    
    @field_validator("description")
    def validate_description(cls, value):
        if not value.strip():
            raise ValueError("A descrição do plano de pagamento não pode ser vazia.")
        
        if len(value) > 500:
            raise ValueError("A descrição do plano de pagamento não pode exceder 500 caracteres.")
        
        return value
        



class PaymentPlanCreate(PaymentPlan, table=True):
    id: int = Field(default=None, primary_key=True)
    create_at: str = Field(default=None, description="The date and time when the payment plan was created")
    update_at: str = Field(default=None, description="The date and time when the payment plan was last updated")