from sqlalchemy import String, DateTime, ForeignKey, Text, func, Index
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class Customer(Base):
    __tablename__="customers"
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"),unique=True,nullable=True)
    name:Mapped[str]=mapped_column(String(120),index=True)
    email:Mapped[str]=mapped_column(String(255),index=True)
    phone:Mapped[str|None]=mapped_column(String(30),nullable=True)
    company:Mapped[str|None]=mapped_column(String(150),nullable=True)
    address:Mapped[str|None]=mapped_column(Text,nullable=True)
    status:Mapped[str]=mapped_column(String(30),default="active",index=True)
    created_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())
    user=relationship("User",back_populates="customer")
    tickets=relationship("Ticket",back_populates="customer")
