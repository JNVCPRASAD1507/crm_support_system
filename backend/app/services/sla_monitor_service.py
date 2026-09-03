
from datetime import datetime, timezone
import logging

from sqlalchemy.orm import Session

from app.models.ticket import Ticket


logger = logging.getLogger(__name__)


class SLAMonitorService:

    def __init__(self, db: Session):
        self.db = db

    # ========================================================
    # GET BREACHED TICKETS
    # ========================================================

    def get_breached_tickets(self):
        """
        Return active tickets whose SLA deadline has passed.
        """

        now = datetime.now(timezone.utc)

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.sla_deadline.is_not(None),
                Ticket.sla_deadline < now,
                Ticket.status.notin_(
                    [
                        "resolved",
                        "closed",
                        "cancelled",
                    ]
                ),
            )
            .order_by(Ticket.sla_deadline.asc())
            .all()
        )

    # ========================================================
    # GET PENDING TICKETS
    # ========================================================

    def get_pending_tickets(self):
        """
        Return active tickets whose SLA deadline
        has not yet passed.
        """

        now = datetime.now(timezone.utc)

        return (
            self.db.query(Ticket)
            .filter(
                Ticket.sla_deadline.is_not(None),
                Ticket.sla_deadline >= now,
                Ticket.status.notin_(
                    [
                        "resolved",
                        "closed",
                        "cancelled",
                    ]
                ),
            )
            .order_by(Ticket.sla_deadline.asc())
            .all()
        )

    # ========================================================
    # CHECK SLA
    # ========================================================

    def check_sla(self) -> dict:
        """
        Check all active tickets and return
        their current SLA state.
        """

        checked_at = datetime.now(timezone.utc)

        breached_tickets = self.get_breached_tickets()
        pending_tickets = self.get_pending_tickets()

        # Log breached tickets
        for ticket in breached_tickets:
            logger.warning(
                "SLA BREACHED | ticket_id=%s | "
                "priority=%s | deadline=%s",
                ticket.id,
                ticket.priority,
                ticket.sla_deadline,
            )

        # Log summary
        logger.info(
            "SLA CHECK | checked_at=%s | "
            "breached=%s | pending=%s",
            checked_at,
            len(breached_tickets),
            len(pending_tickets),
        )

        return {
            "checked_at": checked_at,
            "breached_count": len(breached_tickets),
            "pending_count": len(pending_tickets),
            "breached_ticket_ids": [
                ticket.id
                for ticket in breached_tickets
            ],
            "pending_ticket_ids": [
                ticket.id
                for ticket in pending_tickets
            ],
        }