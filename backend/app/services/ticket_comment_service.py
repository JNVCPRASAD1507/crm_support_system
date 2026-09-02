from sqlalchemy.orm import Session

from app.repositories.ticket_comment_repository import TicketCommentRepository
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentResponse,
    TicketCommentUpdate,
)


class TicketCommentService:

    def __init__(self, db: Session):
        self.repository = TicketCommentRepository(db)

    def create_comment(
        self,
        ticket_id: int,
        user_id: int,
        data: TicketCommentCreate,
    ) -> TicketCommentResponse:

        ticket_comment = self.repository.create(
            ticket_id=ticket_id,
            user_id=user_id,
            comment=data.comment,
        )

        return TicketCommentResponse.model_validate(ticket_comment)

    def get_ticket_comments(
        self,
        ticket_id: int,
    ) -> list[TicketCommentResponse]:

        comments = self.repository.get_by_ticket(ticket_id)

        return [
            TicketCommentResponse.model_validate(comment)
            for comment in comments
        ]

    def get_comment(
        self,
        comment_id: int,
    ) -> TicketCommentResponse | None:

        comment = self.repository.get_by_id(comment_id)

        if not comment:
            return None

        return TicketCommentResponse.model_validate(comment)

    def update_comment(
        self,
        comment_id: int,
        data: TicketCommentUpdate,
    ) -> TicketCommentResponse | None:

        comment = self.repository.get_by_id(comment_id)

        if not comment:
            return None

        updated_comment = self.repository.update(
            ticket_comment=comment,
            comment=data.comment,
        )

        self.repository.db.commit()

        return TicketCommentResponse.model_validate(updated_comment)