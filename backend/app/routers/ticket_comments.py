from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentResponse,
    TicketCommentUpdate,
)
from app.services.ticket_comment_service import TicketCommentService


router = APIRouter(
    prefix="/tickets",
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
    current_user: User = Depends(get_current_user),
):
    service = TicketCommentService(db)

    return service.create_comment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "/{ticket_id}/comments",
    response_model=list[TicketCommentResponse],
)
def get_ticket_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TicketCommentService(db)

    return service.get_ticket_comments(
        ticket_id=ticket_id,
        current_user=current_user,
    )


@router.get(
    "/comments/{comment_id}",
    response_model=TicketCommentResponse,
)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TicketCommentService(db)

    comment = service.get_comment(
        comment_id,
        current_user=current_user,
    )

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
    current_user: User = Depends(get_current_user),
):
    service = TicketCommentService(db)

    comment = service.update_comment(
        comment_id=comment_id,
        data=data,
        current_user=current_user,
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    return comment


@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_200_OK,
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TicketCommentService(db)

    result = service.delete_comment(
        comment_id=comment_id,
        current_user=current_user,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    return result