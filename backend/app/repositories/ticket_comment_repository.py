from sqlalchemy.orm import Session

from app.models.ticket_comment import TicketComment
from app.repositories.base import BaseRepository


class TicketCommentRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        ticket_id: int,
        user_id: int,
        comment: str,
    ) -> TicketComment:

        ticket_comment = TicketComment(
            ticket_id=ticket_id,
            user_id=user_id,
            comment=comment,
        )

        self.db.add(ticket_comment)
        self.db.commit()
        self.db.refresh(ticket_comment)

        return ticket_comment

    def get_by_id(
        self,
        comment_id: int,
    ) -> TicketComment | None:

        return (
            self.db.query(TicketComment)
            .filter(TicketComment.id == comment_id)
            .first()
        )

    def get_by_ticket(
        self,
        ticket_id: int,
    ) -> list[TicketComment]:

        return (
            self.db.query(TicketComment)
            .filter(TicketComment.ticket_id == ticket_id)
            .order_by(TicketComment.created_at.asc())
            .all()
        )

    def update(
        self,
        ticket_comment: TicketComment,
        comment: str,
    ) -> TicketComment:

        ticket_comment.comment = comment

        self.db.flush()
        self.db.refresh(ticket_comment)

        return ticket_comment