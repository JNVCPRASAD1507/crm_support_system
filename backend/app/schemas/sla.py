
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SLABase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    priority: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    response_time_minutes: int = Field(
        ...,
        gt=0,
    )

    resolution_time_minutes: int = Field(
        ...,
        gt=0,
    )

    is_active: bool = True


class SLACreate(SLABase):
    pass


class SLAUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    priority: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    response_time_minutes: int | None = Field(
        default=None,
        gt=0,
    )

    resolution_time_minutes: int | None = Field(
        default=None,
        gt=0,
    )

    is_active: bool | None = None


class SLAResponse(SLABase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime
    updated_at: datetime | None = None
