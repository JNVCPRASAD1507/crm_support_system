from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:

    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def create(
        self,
        *,
        user_id: int | None,
        action: str,
        entity_type: str,
        entity_id: int | None = None,
        description: str | None = None,
        old_data: dict | None = None,
        new_data: dict | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:

        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            old_data=old_data,
            new_data=new_data,
            ip_address=ip_address,
        )

        return self.repository.create(audit_log)

    def get_by_id(
        self,
        audit_log_id: int,
    ) -> AuditLog | None:
        return self.repository.get_by_id(audit_log_id)

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        user_id: int | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
    ) -> list[AuditLog]:

        return self.repository.list(
            skip=skip,
            limit=limit,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
        )

    def count(
        self,
        *,
        user_id: int | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
    ) -> int:

        return self.repository.count(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
        )