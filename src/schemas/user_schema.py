from .base_schema import ( BaseModel, EmailStr, Optional, Enum, field_validator, re )


class UserRole(str, Enum):
    admin = "admin"
    coach = "coach"
    client = "client"


class UserCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.client

    @field_validator("nome")
    def validate_nome(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres.")
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", v):
            raise ValueError("O nome não deve conter números nem caracteres especiais.")
        return v

    @field_validator("email")
    def validate_email(cls, v):
        if not v:
            raise ValueError("Email é obrigatório.")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v.strip()) < 6:
            raise ValueError("password deve ter pelo menos 6 caracteres.")
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):  # não herda de UserCreateSchema para não expor a password
    id: str
    nome: str
    email: EmailStr
    role: UserRole
    ativo: bool

    class Config:
        from_attributes = True