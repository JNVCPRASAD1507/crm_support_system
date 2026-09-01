
from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
)

from app.services.ticket_service import TicketService

from app.core.dependencies import (
    get_current_user,
    require_roles,
)


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


# ============================================================
# CREATE TICKET
# ADMIN / SUPPORT AGENT / CUSTOMER
# ============================================================

@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "support_agent",
            "customer",
        )
    ),
):

    service = TicketService(db)

    ticket = service.create(data)

    db.commit()
    db.refresh(ticket)

    return ticket


# ============================================================
# LIST TICKETS
# ADMIN / SUPPORT AGENT / CUSTOMER
# ============================================================

@router.get(
    "",
    response_model=list[TicketResponse],
)
def list_tickets(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    priority: str | None = None,
    customer_id: int | None = None,
    category_id: int | None = None,
    assigned_agent_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = TicketService(db)

    tickets, total = service.list(
        skip=skip,
        limit=limit,
        status_filter=status_filter,
        priority=priority,
        customer_id=customer_id,
        category_id=category_id,
        assigned_agent_id=assigned_agent_id,
    )

    return tickets


# ============================================================
# GET SINGLE TICKET
# ADMIN / SUPPORT AGENT / CUSTOMER
# ============================================================

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = TicketService(db)

    return service.get(ticket_id)


# ============================================================
# UPDATE TICKET
# ADMIN / SUPPORT AGENT
# ============================================================

@router.put(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "support_agent",
        )
    ),
):

    service = TicketService(db)

    ticket = service.update(
        ticket_id,
        data,
    )

    db.commit()
    db.refresh(ticket)

    return ticket


# ============================================================
# DELETE TICKET
# ADMIN ONLY
# ============================================================

@router.delete(
    "/{ticket_id}",
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    ),
):

    service = TicketService(db)

    result = service.delete(ticket_id)

    db.commit()

    return result
