
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sla import SLA
from app.repositories.sla_repository import SLARepository
from app.schemas.sla import SLACreate, SLAUpdate


class SLAService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = SLARepository(db)

    def get_by_id(self, sla_id: int) -> SLA:
        sla = self.repository.get_by_id(sla_id)

        if not sla:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SLA not found",
            )

        return sla

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ):
        return self.repository.list(
            skip=skip,
            limit=limit,
            active_only=active_only,
        )

    def create(self, data: SLACreate) -> SLA:
        existing = self.repository.get_by_priority(data.priority)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"An active SLA already exists "
                    f"for priority '{data.priority}'"
                ),
            )

        sla = SLA(
            name=data.name,
            description=data.description,
            priority=data.priority,
            response_time_minutes=data.response_time_minutes,
            resolution_time_minutes=data.resolution_time_minutes,
            is_active=data.is_active,
        )

        return self.repository.create(sla)

    def update(
        self,
        sla_id: int,
        data: SLAUpdate,
    ) -> SLA:
        sla = self.get_by_id(sla_id)

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if (
            "priority" in update_data
            and update_data["priority"] != sla.priority
            and update_data.get("is_active", sla.is_active)
        ):
            existing = self.repository.get_by_priority(
                update_data["priority"]
            )

            if existing and existing.id != sla.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"An active SLA already exists "
                        f"for priority "
                        f"'{update_data['priority']}'"
                    ),
                )

        for field, value in update_data.items():
            setattr(sla, field, value)

        return self.repository.update(sla)

    def delete(self, sla_id: int) -> None:
        sla = self.get_by_id(sla_id)

        self.repository.delete(sla)

    def get_sla_for_priority(
        self,
        priority: str,
    ) -> SLA:
        sla = self.repository.get_by_priority(priority)

        if not sla:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"No active SLA found for "
                    f"priority '{priority}'"
                ),
            )

        return sla

    def calculate_deadlines(
        self,
        priority: str,
        start_time: datetime | None = None,
    ) -> dict:
        sla = self.get_sla_for_priority(priority)

        if start_time is None:
            start_time = datetime.now(timezone.utc)

        response_deadline = (
            start_time
            + timedelta(minutes=sla.response_time_minutes)
        )

        resolution_deadline = (
            start_time
            + timedelta(minutes=sla.resolution_time_minutes)
        )

        return {
            "sla_id": sla.id,
            "sla_name": sla.name,
            "priority": sla.priority,
            "start_time": start_time,
            "response_deadline": response_deadline,
            "resolution_deadline": resolution_deadline,
        }