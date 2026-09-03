from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int | None = None

    action: str

    entity_type: str

    entity_id: int | None = None

    description: str | None = None

    old_data: dict | None = None

    new_data: dict | None = None

    ip_address: str | None = None

    created_at: datetime