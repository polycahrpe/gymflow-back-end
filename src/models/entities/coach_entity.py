from .main_entity import (Field, SQLModel, field_validator, re)


class CoachRegister(SQLModel):
    email: str = Field(..., description="The email of the coach")
    especiality: str = Field(..., description="The especiality of the coach")

    @field_validator("email")
    def validate_email(cls, value):
        """Valida o campo `email` no cadastro do coach."""
        if not value.strip():
            raise ValueError("O email nao pode ser vazio.")
        
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
            raise ValueError("O email nao e valido.")
        
        return value

    @field_validator("especiality")
    def validate_especiality(cls, value):
        if not value.strip():
            raise ValueError("A especialidade nao pode ser vazia.")
        
        if len(value) > 100:
            raise ValueError("A especialidade nao pode exceder 100 caracteres.")
        
        return value