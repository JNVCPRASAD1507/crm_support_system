from .base import BaseRepository
from app.models.customer import Customer
class CustomerRepository(BaseRepository):
    def list(self,search=None,status=None,skip=0,limit=20):
        q=self.db.query(Customer)
        if search: q=q.filter((Customer.name.ilike(f"%{search}%"))|(Customer.email.ilike(f"%{search}%"))|(Customer.company.ilike(f"%{search}%")))
        if status: q=q.filter(Customer.status==status)
        return q.offset(skip).limit(limit).all(),q.count()
