from .base import BaseRepository
from app.models.user import User
class UserRepository(BaseRepository):
    def by_email(self,email): return self.db.query(User).filter(User.email==email).first()
    def agents(self): return self.db.query(User).filter(User.role=="support_agent",User.is_active==True).all()
