from .main_entity import (Field, SQLModel, field_validator)


class Login(SQLModel):
    # Telefone pode conter zeros à esquerda e pode ser enviado como string;
    # por isso tratamos como `str`.
    number: str = Field(..., description="O numero de celular do usuario")
    password: str = Field(..., description="A senha do usuario")

    @field_validator("number")
    @classmethod
    def validate_number(cls, number: str):
        if not number.strip():
            raise ValueError("O numero de celular nao pode ser vazio.")
        return number

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        if not password.strip():
            raise ValueError("A senha nao pode ser vazia.")
        return password