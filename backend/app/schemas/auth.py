from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8)
    phone: str | None = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    role: str
    is_active: bool
    created_at: datetime


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)