from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentResponse,
    TicketCommentUpdate,
)
from app.services.ticket_comment_service import TicketCommentService


router = APIRouter(
    prefix="/tickets_comments",
    tags=["Ticket Comments"],
)


@router.post(
    "/{ticket_id}/comments",
    response_model=TicketCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket_comment(
    ticket_id: int,
    data: TicketCommentCreate,
    db: Session = Depends(get_db),
):
    service = TicketCommentService(db)

    # Temporary until JWT current-user dependency is connected
    user_id = 5

    return service.create_comment(
        ticket_id=ticket_id,
        user_id=user_id,
        data=data,
    )


@router.get(
    "/{ticket_id}/comments",
    response_model=list[TicketCommentResponse],
)
def get_ticket_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    service = TicketCommentService(db)

    return service.get_ticket_comments(ticket_id)


@router.get(
    "/comments/{comment_id}",
    response_model=TicketCommentResponse,
)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    service = TicketCommentService(db)

    comment = service.get_comment(comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    return comment


@router.put(
    "/comments/{comment_id}",
    response_model=TicketCommentResponse,
)
def update_comment(
    comment_id: int,
    data: TicketCommentUpdate,
    db: Session = Depends(get_db),
):
    service = TicketCommentService(db)

    comment = service.update_comment(
        comment_id=comment_id,
        data=data,
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    return comment