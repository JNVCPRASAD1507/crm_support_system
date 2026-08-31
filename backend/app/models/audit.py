from sqlalchemy import String,Text,DateTime,ForeignKey,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"),nullable=True,index=True)
    action:Mapped[str]=mapped_column(String(80),index=True)
    entity:Mapped[str]=mapped_column(String(80),index=True)
    entity_id:Mapped[int]=mapped_column(index=True)
    previous_value:Mapped[str|None]=mapped_column(Text,nullable=True)
    new_value:Mapped[str|None]=mapped_column(Text,nullable=True)
    timestamp:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)
    user=relationship("User")
