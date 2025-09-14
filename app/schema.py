#app/schema.py
from fastapi import Form
from pydantic import BaseModel, Field


class RegisterFormSchema(BaseModel):
    user: str = Field(example="user@example.com")
    password: str = Field(min_length=5)

    @classmethod
    def as_form(cls, user: str = Form(...), password: str = Form(...)):
        return cls(user=user, password=password)

    class Config:
        from_attributes = True


class LoginFormSchema(BaseModel):
    user: str
    password: str

    @classmethod
    def as_form(cls, user: str = Form(...), password: str = Form(...)):
        return cls(user=user, password=password)

    class Config:
        from_attributes = True
