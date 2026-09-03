from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.ticket_comment_repository import TicketCommentRepository
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentResponse,
    TicketCommentUpdate,
)


class TicketCommentService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = TicketCommentRepository(db)

    # ============================================================
    # ACCESS CONTROL
    # ============================================================

    @staticmethod
    def _can_access_ticket(
        ticket: Ticket,
        user: User,
    ) -> bool:

        # Admin can access everything
        if user.role == "admin":
            return True

        # Support agent can access assigned tickets
        if user.role == "support_agent":
            return ticket.assigned_agent_id == user.id

        # Customer can access their own tickets
        if user.role == "customer":
            return (
                ticket.customer is not None
                and ticket.customer.user_id == user.id
            )

        return False

    @staticmethod
    def _can_modify_comment(
        comment,
        user: User,
    ) -> bool:

        # Admin can modify any comment
        if user.role == "admin":
            return True

        # Normal users can modify only their own comment
        return comment.user_id == user.id

    # ============================================================
    # GET TICKET
    # ============================================================

    def _get_ticket_or_404(
        self,
        ticket_id: int,
    ) -> Ticket:

        ticket = self.db.get(Ticket, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        return ticket

    # ============================================================
    # CREATE COMMENT
    # ============================================================

    def create_comment(
        self,
        ticket_id: int,
        user_id: int,
        data: TicketCommentCreate,
    ) -> TicketCommentResponse:

        ticket = self._get_ticket_or_404(ticket_id)

        user = self.db.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not self._can_access_ticket(ticket, user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        if ticket.status in {"closed", "cancelled"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Comments cannot be added to a closed "
                    "or cancelled ticket"
                ),
            )

        comment_text = data.comment.strip()

        if not comment_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment cannot be empty",
            )

        comment = self.repository.create(
            ticket_id=ticket_id,
            user_id=user_id,
            comment=comment_text,
        )

        return TicketCommentResponse.model_validate(comment)

    # ============================================================
    # GET ALL COMMENTS
    # ============================================================

    def get_ticket_comments(
        self,
        ticket_id: int,
        current_user: User,
    ) -> list[TicketCommentResponse]:

        ticket = self._get_ticket_or_404(ticket_id)

        if not self._can_access_ticket(ticket, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        comments = self.repository.get_by_ticket(ticket_id)

        return [
            TicketCommentResponse.model_validate(comment)
            for comment in comments
        ]

    # ============================================================
    # GET SINGLE COMMENT
    # ============================================================

    def get_comment(
        self,
        comment_id: int,
        current_user: User,
    ) -> TicketCommentResponse | None:

        comment = self.repository.get_by_id(comment_id)

        if not comment:
            return None

        if not self._can_access_ticket(
            comment.ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        return TicketCommentResponse.model_validate(comment)

    # ============================================================
    # UPDATE COMMENT
    # ============================================================

    def update_comment(
        self,
        comment_id: int,
        data: TicketCommentUpdate,
        current_user: User,
    ) -> TicketCommentResponse | None:

        comment = self.repository.get_by_id(comment_id)

        if not comment:
            return None

        if not self._can_access_ticket(
            comment.ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        if not self._can_modify_comment(
            comment,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only modify your own comments",
            )

        if comment.ticket.status in {"closed", "cancelled"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Comments cannot be modified on a closed "
                    "or cancelled ticket"
                ),
            )

        comment_text = data.comment.strip()

        if not comment_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment cannot be empty",
            )

        updated_comment = self.repository.update(
            ticket_comment=comment,
            comment=comment_text,
        )

        self.db.commit()
        self.db.refresh(updated_comment)

        return TicketCommentResponse.model_validate(
            updated_comment
        )

    # ============================================================
    # DELETE COMMENT
    # ============================================================

    def delete_comment(
        self,
        comment_id: int,
        current_user: User,
    ) -> dict | None:

        comment = self.repository.get_by_id(comment_id)

        if not comment:
            return None

        if not self._can_access_ticket(
            comment.ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        if not self._can_modify_comment(
            comment,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own comments",
            )

        self.repository.delete(comment)

        self.db.commit()

        return {
            "message": "Comment deleted successfully"
        }