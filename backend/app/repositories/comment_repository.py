from .base import BaseRepository
from app.models.comment import TicketComment
class CommentRepository(BaseRepository):
    def by_ticket(self,ticket_id): return self.db.query(TicketComment).filter(TicketComment.ticket_id==ticket_id).order_by(TicketComment.created_at).all()
