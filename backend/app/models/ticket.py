from sqlalchemy import String,Text,DateTime,ForeignKey,func,Index
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class Ticket(Base):
    __tablename__="tickets"
    id:Mapped[int]=mapped_column(primary_key=True)
    customer_id:Mapped[int]=mapped_column(ForeignKey("customers.id",ondelete="CASCADE"),index=True)
    assigned_agent_id:Mapped[int|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"),nullable=True,index=True)
    category_id:Mapped[int|None]=mapped_column(ForeignKey("categories.id",ondelete="SET NULL"),nullable=True,index=True)
    subject:Mapped[str]=mapped_column(String(200))
    description:Mapped[str]=mapped_column(Text)
    priority:Mapped[str]=mapped_column(String(20),default="medium",index=True)
    status:Mapped[str]=mapped_column(String(30),default="open",index=True)
    created_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)
    updated_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    resolved_at:Mapped[object|None]=mapped_column(DateTime(timezone=True),nullable=True)
    sla_deadline:Mapped[object|None]=mapped_column(DateTime(timezone=True),nullable=True,index=True)
    first_response_at:Mapped[object|None]=mapped_column(DateTime(timezone=True),nullable=True)
    customer=relationship("Customer",back_populates="tickets")
    agent=relationship("User",foreign_keys=[assigned_agent_id])
    category=relationship("Category",back_populates="tickets")
    comments=relationship("TicketComment",back_populates="ticket",cascade="all, delete-orphan")
    attachments=relationship("TicketAttachment",back_populates="ticket",cascade="all, delete-orphan")
