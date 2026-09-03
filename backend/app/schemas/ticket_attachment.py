
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TicketAttachmentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    ticket_id: int
    uploaded_by_id: int

    file_name: str
    file_size: int
    file_type: str

    uploaded_at: datetime
