from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TicketCommentCreate(BaseModel):
    comment: str = Field(
        ...,
        min_length=1,
        description="Comment text",
    )


class TicketCommentUpdate(BaseModel):
    comment: str = Field(
        ...,
        min_length=1,
        description="Updated comment text",
    )


class TicketCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    user_id: int
    comment: str
    created_at: datetime
    updated_at: datetime