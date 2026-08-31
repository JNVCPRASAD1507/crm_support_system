from sqlalchemy import String,Integer,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from app.db.session import Base
class SLAPolicy(Base):
    __tablename__="sla_policies"
    id:Mapped[int]=mapped_column(primary_key=True)
    priority:Mapped[str]=mapped_column(String(20),unique=True,index=True)
    response_hours:Mapped[int]=mapped_column(Integer)
    resolution_hours:Mapped[int]=mapped_column(Integer)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
