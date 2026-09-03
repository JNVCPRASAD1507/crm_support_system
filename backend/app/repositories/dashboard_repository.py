from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.ticket import Ticket
from app.models.user import User


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_total_tickets(self) -> int:
        return self.db.query(func.count(Ticket.id)).scalar() or 0

    def get_tickets_by_status(self, status: str) -> int:
        return (
            self.db.query(func.count(Ticket.id))
            .filter(Ticket.status == status)
            .scalar()
            or 0
        )

    def get_tickets_by_priority(self, priority: str) -> int:
        return (
            self.db.query(func.count(Ticket.id))
            .filter(Ticket.priority == priority)
            .scalar()
            or 0
        )

    def get_unassigned_tickets(self) -> int:
        return (
            self.db.query(func.count(Ticket.id))
            .filter(Ticket.assigned_agent_id.is_(None))
            .scalar()
            or 0
        )

    def get_total_customers(self) -> int:
        return self.db.query(func.count(Customer.id)).scalar() or 0

    def get_active_customers(self) -> int:
        return (
            self.db.query(func.count(Customer.id))
            .filter(Customer.status == "active")
            .scalar()
            or 0
        )

    def get_total_agents(self) -> int:
        return (
            self.db.query(func.count(User.id))
            .filter(User.role == "agent")
            .scalar()
            or 0
        )

    def get_active_agents(self) -> int:
        return (
            self.db.query(func.count(User.id))
            .filter(
                User.role == "agent",
                User.is_active.is_(True),
            )
            .scalar()
            or 0
        )

    def get_sla_breached(self) -> int:
        now = datetime.now(timezone.utc)

        return (
            self.db.query(func.count(Ticket.id))
            .filter(
                Ticket.sla_deadline.is_not(None),
                Ticket.sla_deadline < now,
                Ticket.status.notin_(["resolved", "closed"]),
            )
            .scalar()
            or 0
        )

    def get_sla_pending(self) -> int:
        now = datetime.now(timezone.utc)

        return (
            self.db.query(func.count(Ticket.id))
            .filter(
                Ticket.sla_deadline.is_not(None),
                Ticket.sla_deadline >= now,
                Ticket.status.notin_(["resolved", "closed"]),
            )
            .scalar()
            or 0
        )

    def get_first_response_pending(self) -> int:
        return (
            self.db.query(func.count(Ticket.id))
            .filter(
                Ticket.first_response_at.is_(None),
                Ticket.status.notin_(["resolved", "closed"]),
            )
            .scalar()
            or 0
        )