
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    company: str | None = Field(
        default=None,
        max_length=150,
    )

    address: str | None = None

    status: str = "active"


class CustomerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    company: str | None = Field(
        default=None,
        max_length=150,
    )

    address: str | None = None

    status: str | None = None


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str | None
    company: str | None
    address: str | None
    status: str
    created_at: datetime
