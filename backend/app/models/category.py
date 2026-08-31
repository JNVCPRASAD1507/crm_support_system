from sqlalchemy import String,Text,Boolean
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class Category(Base):
    __tablename__="categories"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(80),unique=True,index=True)
    description:Mapped[str|None]=mapped_column(Text,nullable=True)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    tickets=relationship("Ticket",back_populates="category")
