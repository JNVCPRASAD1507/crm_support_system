from datetime import datetime, timezone
from fastapi import HTTPException
from app.models.ticket import Ticket
from app.models.user import User

TRANS = {
    "open": {"in_progress", "cancelled"},
    "in_progress": {"waiting_for_customer", "resolved", "cancelled"},
    "waiting_for_customer": {"in_progress", "cancelled"},
    "resolved": {"closed"},
    "closed": set(),
    "cancelled": set(),
}


class TicketService:
    @staticmethod
    def ensure_access(ticket, user, write=False):
        if user.role == "admin":
            return
        if user.role == "customer":
            if not ticket.customer or ticket.customer.user_id != user.id:
                raise HTTPException(403, "You can only access your own tickets")
            if write and ticket.status in ("closed", "cancelled"):
                raise HTTPException(400, "Ticket cannot be modified")
        elif user.role == "support_agent":
            if ticket.assigned_agent_id != user.id:
                raise HTTPException(403, "Ticket is not assigned to you")
            if write and ticket.status in ("closed", "cancelled"):
                raise HTTPException(400, "Ticket cannot be modified")

    @staticmethod
    def create(db, data, user):
        customer_id = (
            user.customer.id
            if user.role == "customer" and user.customer
            else data.get("customer_id")
        )
        if not customer_id:
            raise HTTPException(400, "Customer profile is required")
        t = Ticket(
            customer_id=customer_id,
            subject=data["subject"],
            description=data["description"],
            category_id=data.get("category_id"),
            priority=data.get("priority", "medium"),
        )

    @staticmethod
    def transition(db, ticket, new_status, user):
        TicketService.ensure_access(ticket, user, True)
        old = ticket.status
        if new_status == old:
            return ticket
        if new_status not in TRANS.get(old, set()):
            raise HTTPException(
                400, f"Invalid status transition: {old} -> {new_status}"
            )
        ticket.status = new_status
        if new_status == "resolved":
            ticket.resolved_at = datetime.now(timezone.utc)
