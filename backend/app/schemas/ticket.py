from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    customer_id: int
    category_id: int | None = None

    subject: str = Field(
        min_length=3,
        max_length=200,
    )

    description: str = Field(
        min_length=5,
    )

    priority: str = Field(
        default="medium",
    )


class TicketUpdate(BaseModel):
    category_id: int | None = None
    assigned_agent_id: int | None = None

    subject: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        min_length=5,
    )

    priority: str | None = None
    status: str | None = None


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    customer_id: int
    assigned_agent_id: int | None
    category_id: int | None

    subject: str
    description: str

    priority: str
    status: str

    created_at: datetime
    updated_at: datetime

    resolved_at: datetime | None
    sla_deadline: datetime | None
    first_response_at: datetime | None


class TicketListResponse(BaseModel):
    items: list[TicketResponse]

    total: int

    skip: int

    limit: int

    page: int

    pages: int
