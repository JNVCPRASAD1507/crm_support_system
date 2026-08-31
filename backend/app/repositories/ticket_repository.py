from .base import BaseRepository
from app.models.ticket import Ticket
class TicketRepository(BaseRepository):
    def query(self): return self.db.query(Ticket)
    def list(self,filters,skip,limit):
        q=self.query()
        if filters.get("search"): q=q.filter((Ticket.subject.ilike(f"%{filters['search']}%"))|(Ticket.description.ilike(f"%{filters['search']}%")))
        for k in ["status","priority","category_id","assigned_agent_id","customer_id"]:
            if filters.get(k) is not None: q=q.filter(getattr(Ticket,k)==filters[k])
        total=q.count(); return q.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all(),total
