
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.ticket import Ticket
from app.models.user import User

from app.repositories.ticket_repository import TicketRepository


class TicketService:

    ALLOWED_PRIORITIES = {
        "low",
        "medium",
        "high",
        "urgent",
    }

    ALLOWED_STATUSES = {
        "open",
        "in_progress",
        "pending",
        "resolved",
        "closed",
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = TicketRepository(db)

    # ============================================================
    # CREATE TICKET
    # ============================================================

    def create(self, data):

        # --------------------------------------------------------
        # Validate customer
        # --------------------------------------------------------

        from app.models.customer import Customer

        customer = (
            self.db.query(Customer)
            .filter(Customer.id == data.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        # --------------------------------------------------------
        # Validate category
        # --------------------------------------------------------

        if data.category_id is not None:

            category = (
                self.db.query(Category)
                .filter(Category.id == data.category_id)
                .first()
            )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

            if not category.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category is inactive",
                )

        # --------------------------------------------------------
        # Validate priority
        # --------------------------------------------------------

        priority = data.priority.lower()

        if priority not in self.ALLOWED_PRIORITIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid priority. Allowed values: "
                    "low, medium, high, urgent"
                ),
            )

        # --------------------------------------------------------
        # Create ticket
        # --------------------------------------------------------

        return self.repository.create(
            customer_id=data.customer_id,
            category_id=data.category_id,
            subject=data.subject,
            description=data.description,
            priority=priority,
        )

    # ============================================================
    # GET TICKET
    # ============================================================

    def get(self, ticket_id: int):

        ticket = self.repository.get_by_id(ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        return ticket

    # ============================================================
    # LIST TICKETS
    # ============================================================

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        status_filter: str | None = None,
        priority: str | None = None,
        customer_id: int | None = None,
        category_id: int | None = None,
        assigned_agent_id: int | None = None,
    ):

        # --------------------------------------------------------
        # Validate status
        # --------------------------------------------------------

        if status_filter is not None:

            status_filter = status_filter.lower()

            if status_filter not in self.ALLOWED_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid status. Allowed values: "
                        "open, in_progress, pending, "
                        "resolved, closed"
                    ),
                )

        # --------------------------------------------------------
        # Validate priority
        # --------------------------------------------------------

        if priority is not None:

            priority = priority.lower()

            if priority not in self.ALLOWED_PRIORITIES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid priority. Allowed values: "
                        "low, medium, high, urgent"
                    ),
                )

        return self.repository.list(
            skip=skip,
            limit=limit,
            status=status_filter,
            priority=priority,
            customer_id=customer_id,
            category_id=category_id,
            assigned_agent_id=assigned_agent_id,
        )

    # ============================================================
    # UPDATE TICKET
    # ============================================================

    def update(
        self,
        ticket_id: int,
        data,
    ):

        ticket = self.get(ticket_id)

        # --------------------------------------------------------
        # Validate category
        # --------------------------------------------------------

        if data.category_id is not None:

            category = (
                self.db.query(Category)
                .filter(Category.id == data.category_id)
                .first()
            )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )

            if not category.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category is inactive",
                )

        # --------------------------------------------------------
        # Validate assigned agent
        # --------------------------------------------------------

        if data.assigned_agent_id is not None:

            agent = (
                self.db.query(User)
                .filter(User.id == data.assigned_agent_id)
                .first()
            )

            if not agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assigned agent not found",
                )

            if not agent.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assigned agent is inactive",
                )

        # --------------------------------------------------------
        # Validate priority
        # --------------------------------------------------------

        priority = data.priority

        if priority is not None:

            priority = priority.lower()

            if priority not in self.ALLOWED_PRIORITIES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid priority. Allowed values: "
                        "low, medium, high, urgent"
                    ),
                )

        # --------------------------------------------------------
        # Validate status
        # --------------------------------------------------------

        new_status = data.status

        if new_status is not None:

            new_status = new_status.lower()

            if new_status not in self.ALLOWED_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid status. Allowed values: "
                        "open, in_progress, pending, "
                        "resolved, closed"
                    ),
                )

        # --------------------------------------------------------
        # Handle resolved_at
        # --------------------------------------------------------

        resolved_at = ticket.resolved_at

        if (
            new_status in {"resolved", "closed"}
            and ticket.resolved_at is None
        ):
            resolved_at = datetime.now(timezone.utc)

        elif (
            new_status is not None
            and new_status not in {"resolved", "closed"}
        ):
            resolved_at = None

        # --------------------------------------------------------
        # Update ticket
        # --------------------------------------------------------

        updated_ticket = self.repository.update(
            ticket,
            category_id=data.category_id,
            assigned_agent_id=data.assigned_agent_id,
            subject=data.subject,
            description=data.description,
            priority=priority,
            status=new_status,
        )

        # --------------------------------------------------------
        # Update resolved_at
        # --------------------------------------------------------

        updated_ticket.resolved_at = resolved_at

        self.db.flush()
        self.db.refresh(updated_ticket)

        return updated_ticket

    # ============================================================
    # DELETE TICKET
    # ============================================================

    def delete(self, ticket_id: int):

        ticket = self.get(ticket_id)

        self.repository.delete(ticket)

        return {
            "message": "Ticket deleted successfully"
        }
        
        