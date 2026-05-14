from .base_schema import BaseModel


class AccessCodeResponseSchema(BaseModel):
    id: str
    code: str
    usado: bool

    class Config:
        from_attributes = True