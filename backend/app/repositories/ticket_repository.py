from app.models.ticket import Ticket

from .base import BaseRepository


class TicketRepository(BaseRepository):

    def get_by_id(self, ticket_id: int):
        return (
            self.db.query(Ticket)
            .filter(Ticket.id == ticket_id)
            .first()
        )

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        customer_id: int | None = None,
        category_id: int | None = None,
        assigned_agent_id: int | None = None,
    ):
        query = self.db.query(Ticket)

        # Search by subject or description
        if search is not None and search.strip():
            search_term = f"%{search.strip()}%"

            query = query.filter(
                Ticket.subject.ilike(search_term)
                | Ticket.description.ilike(search_term)
            )

        # Status filter
        if status is not None:
            query = query.filter(
                Ticket.status == status
            )

        # Priority filter
        if priority is not None:
            query = query.filter(
                Ticket.priority == priority
            )

        # Customer filter
        if customer_id is not None:
            query = query.filter(
                Ticket.customer_id == customer_id
            )

        # Category filter
        if category_id is not None:
            query = query.filter(
                Ticket.category_id == category_id
            )

        # Assigned agent filter
        if assigned_agent_id is not None:
            query = query.filter(
                Ticket.assigned_agent_id == assigned_agent_id
            )

        total = query.count()

        items = (
            query
            .order_by(Ticket.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    def create(
        self,
        *,
        customer_id: int,
        category_id: int | None,
        subject: str,
        description: str,
        priority: str,
    ):
        ticket = Ticket(
            customer_id=customer_id,
            category_id=category_id,
            subject=subject,
            description=description,
            priority=priority,
            status="open",
        )

        return self.add(ticket)

    def update(
        self,
        ticket: Ticket,
        *,
        customer_id: int | None = None,
        category_id: int | None = None,
        assigned_agent_id: int | None = None,
        subject: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        status: str | None = None,
    ):
        if customer_id is not None:
            ticket.customer_id = customer_id

        if category_id is not None:
            ticket.category_id = category_id

        if assigned_agent_id is not None:
            ticket.assigned_agent_id = assigned_agent_id

        if subject is not None:
            ticket.subject = subject

        if description is not None:
            ticket.description = description

        if priority is not None:
            ticket.priority = priority

        if status is not None:
            ticket.status = status

        self.db.flush()
        self.db.refresh(ticket)

        return ticket

    def delete(self, ticket: Ticket):
        self.db.delete(ticket)
        self.db.flush()
        
        