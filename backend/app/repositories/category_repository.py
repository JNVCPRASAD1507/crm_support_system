from .base import BaseRepository
from app.models.category import Category
class CategoryRepository(BaseRepository):
    def list(self,search=None):
        q=self.db.query(Category)
        if search:q=q.filter(Category.name.ilike(f"%{search}%"))
        return q.order_by(Category.name).all()
