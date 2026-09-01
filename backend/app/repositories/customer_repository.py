from .base import BaseRepository
from app.models.customer import Customer


class CustomerRepository(BaseRepository):

    def list(
        self,
        search=None,
        status=None,
        skip=0,
        limit=20,
    ):
        q = self.db.query(Customer)

        if search:
            q = q.filter(
                (Customer.name.ilike(f"%{search}%"))
                | (Customer.email.ilike(f"%{search}%"))
                | (Customer.company.ilike(f"%{search}%"))
            )

        if status:
            q = q.filter(
                Customer.status == status
            )

        total = q.count()

        items = (
            q.offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    def by_user_id(self, user_id: int):
        return (
            self.db.query(Customer)
            .filter(Customer.user_id == user_id)
            .first()
        )

    def create(
        self,
        *,
        user_id: int,
        name: str,
        email: str,
        phone: str | None = None,
        status: str = "active",
    ):
        customer = Customer(
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            status=status,
        )

        return self.add(customer)