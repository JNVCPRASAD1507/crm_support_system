
from sqlalchemy.orm import Session

from app.models.sla import SLA
from app.repositories.base import BaseRepository


class SLARepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, sla_id: int):
        return (
            self.db.query(SLA)
            .filter(SLA.id == sla_id)
            .first()
        )

    def get_by_priority(self, priority: str):
        return (
            self.db.query(SLA)
            .filter(
                SLA.priority == priority,
                SLA.is_active.is_(True),
            )
            .first()
        )

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ):
        query = self.db.query(SLA)

        if active_only:
            query = query.filter(SLA.is_active.is_(True))

        return (
            query
            .order_by(SLA.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, sla: SLA):
        return self.add(sla)

    def update(self, sla: SLA):
        self.db.flush()
        self.db.refresh(sla)
        return sla

    def delete(self, sla: SLA):
        self.db.delete(sla)
        self.db.flush()
