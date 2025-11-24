from pydantic import BaseModel

class LoginModel(BaseModel):
    name: str
    password: str

class RegisterModel(BaseModel):
    name: str
    email: str
    password: str