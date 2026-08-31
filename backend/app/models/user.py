from sqlalchemy import String, Boolean, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    full_name:Mapped[str]=mapped_column(String(120))
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True)
    phone:Mapped[str|None]=mapped_column(String(30),nullable=True)
    password_hash:Mapped[str]=mapped_column(String(255))
    role:Mapped[str]=mapped_column(String(30),index=True,default="customer")
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,index=True)
    created_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())
    customer:Mapped["Customer|None"]=relationship(back_populates="user",uselist=False)
