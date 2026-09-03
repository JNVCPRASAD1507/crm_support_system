from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, audit_log: AuditLog) -> AuditLog:
        self.db.add(audit_log)
        self.db.flush()
        self.db.refresh(audit_log)

        return audit_log

    def get_by_id(self, audit_log_id: int) -> AuditLog | None:
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.id == audit_log_id)
            .first()
        )

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

        query = self.db.query(AuditLog)

        if user_id is not None:
            query = query.filter(
                AuditLog.user_id == user_id
            )

        if action is not None:
            query = query.filter(
                AuditLog.action == action
            )

        if entity_type is not None:
            query = query.filter(
                AuditLog.entity_type == entity_type
            )

        if entity_id is not None:
            query = query.filter(
                AuditLog.entity_id == entity_id
            )

        return (
            query
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(
        self,
        *,
        user_id: int | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
    ) -> int:

        query = self.db.query(AuditLog)

        if user_id is not None:
            query = query.filter(
                AuditLog.user_id == user_id
            )

        if action is not None:
            query = query.filter(
                AuditLog.action == action
            )

        if entity_type is not None:
            query = query.filter(
                AuditLog.entity_type == entity_type
            )

        if entity_id is not None:
            query = query.filter(
                AuditLog.entity_id == entity_id
            )

        return query.count()