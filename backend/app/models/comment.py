from sqlalchemy import Text,DateTime,ForeignKey,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class TicketComment(Base):
    __tablename__="ticket_comments"
    id:Mapped[int]=mapped_column(primary_key=True)
    ticket_id:Mapped[int]=mapped_column(ForeignKey("tickets.id",ondelete="CASCADE"),index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    comment:Mapped[str]=mapped_column(Text)
    created_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    ticket=relationship("Ticket",back_populates="comments")
    user=relationship("User")
