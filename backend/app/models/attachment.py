from sqlalchemy import String,DateTime,ForeignKey,BigInteger,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class TicketAttachment(Base):
    __tablename__="ticket_attachments"
    id:Mapped[int]=mapped_column(primary_key=True)
    ticket_id:Mapped[int]=mapped_column(ForeignKey("tickets.id",ondelete="CASCADE"),index=True)
    uploaded_by_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    file_name:Mapped[str]=mapped_column(String(255))
    file_path:Mapped[str]=mapped_column(String(500))
    file_size:Mapped[int]=mapped_column(BigInteger)
    file_type:Mapped[str]=mapped_column(String(100))
    uploaded_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())
    ticket=relationship("Ticket",back_populates="attachments")
    uploaded_by=relationship("User")
