
from datetime import datetime, timedelta, timezone
import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.ticket import Ticket
from app.models.user import User

from app.repositories.ticket_repository import TicketRepository


# Backward-compatible export used by business-rule tests.
TRANS = {
    "open": {
        "in_progress",
        "cancelled",
    },
    "in_progress": {
        "waiting_for_customer",
        "resolved",
        "cancelled",
    },
    "waiting_for_customer": {
        "in_progress",
        "cancelled",
    },
    "resolved": {
        "closed",
    },
    "closed": set(),
    "cancelled": set(),
}


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
        "waiting_for_customer",
        "resolved",
        "closed",
        "cancelled",
    }

    ALLOWED_STATUS_TRANSITIONS = {
        "open": {
            "in_progress",
            "cancelled",
        },
        "in_progress": {
            "waiting_for_customer",
            "resolved",
            "cancelled",
        },
        "waiting_for_customer": {
            "in_progress",
            "cancelled",
        },
        "resolved": {
            "closed",
        },
        "closed": set(),
        "cancelled": set(),
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = TicketRepository(db)

    # ============================================================
    # CREATE TICKET
    # ============================================================

    def create(self, data):

        from app.models.customer import Customer
        from app.services.sla_service import SLAService

        # --------------------------------------------------------
        # Validate customer
        # --------------------------------------------------------

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
        # Get SLA for priority
        # --------------------------------------------------------

        sla_service = SLAService(self.db)

        sla = sla_service.get_sla_for_priority(
            priority
        )

        # --------------------------------------------------------
        # Calculate SLA deadline
        # --------------------------------------------------------

        start_time = datetime.now(timezone.utc)

        sla_deadline = (
            start_time
            + timedelta(
                minutes=sla.resolution_time_minutes
            )
        )

        # --------------------------------------------------------
        # Create ticket
        # --------------------------------------------------------

        ticket = self.repository.create(
            customer_id=data.customer_id,
            category_id=data.category_id,
            subject=data.subject,
            description=data.description,
            priority=priority,
        )

        # --------------------------------------------------------
        # Assign SLA deadline
        # --------------------------------------------------------

        ticket.sla_deadline = sla_deadline

        self.db.flush()
        self.db.refresh(ticket)

        return ticket

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
        search: str | None = None,
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
                        "open, in_progress, waiting_for_customer, "
                        "resolved, closed, cancelled"
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

        # --------------------------------------------------------
        # Get paginated tickets
        # --------------------------------------------------------

        items, total = self.repository.list(
            skip=skip,
            limit=limit,
            search=search,
            status=status_filter,
            priority=priority,
            customer_id=customer_id,
            category_id=category_id,
            assigned_agent_id=assigned_agent_id,
        )

        # --------------------------------------------------------
        # Calculate pagination
        # --------------------------------------------------------

        page = (skip // limit) + 1

        pages = (
            math.ceil(total / limit)
            if total > 0
            else 0
        )

        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "page": page,
            "pages": pages,
        }

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

            if agent.role not in {
                "admin",
                "support_agent",
            }:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is not an eligible support agent",
                )

        # --------------------------------------------------------
        # Validate priority
        # --------------------------------------------------------

        priority = (
            data.priority.lower()
            if data.priority is not None
            else None
        )

        if (
            priority is not None
            and priority not in self.ALLOWED_PRIORITIES
        ):
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

        new_status = (
            data.status.lower()
            if data.status is not None
            else None
        )

        resolved_at = ticket.resolved_at

        if new_status is not None:

            if new_status not in self.ALLOWED_STATUSES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Invalid status. Allowed values: "
                        "open, in_progress, "
                        "waiting_for_customer, resolved, "
                        "closed, cancelled"
                    ),
                )

            current_status = ticket.status

            if new_status != current_status:

                allowed_next_statuses = (
                    self.ALLOWED_STATUS_TRANSITIONS.get(
                        current_status,
                        set(),
                    )
                )

                if new_status not in allowed_next_statuses:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Invalid status transition: "
                            f"{current_status} → {new_status}"
                        ),
                    )

                # ------------------------------------------------
                # Handle resolved_at
                # ------------------------------------------------

                if (
                    new_status in {
                        "resolved",
                        "closed",
                    }
                    and ticket.resolved_at is None
                ):
                    resolved_at = datetime.now(
                        timezone.utc
                    )

                elif new_status not in {
                    "resolved",
                    "closed",
                }:
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
