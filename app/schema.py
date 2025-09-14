#app/schema.py
from pydantic import BaseModel

class UserSchema(BaseModel):
    user : str
    password : str

    class Config:
        from_attributes = True