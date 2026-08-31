from sqlalchemy import String,Text,Boolean,DateTime,ForeignKey,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
class Notification(Base):
    __tablename__="notifications"
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    title:Mapped[str]=mapped_column(String(160))
    message:Mapped[str]=mapped_column(Text)
    type:Mapped[str]=mapped_column(String(40),default="info")
    is_read:Mapped[bool]=mapped_column(Boolean,default=False,index=True)
    created_at:Mapped[object]=mapped_column(DateTime(timezone=True),server_default=func.now())
    user=relationship("User")
