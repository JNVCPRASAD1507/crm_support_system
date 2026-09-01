from .base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):

    def by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create(
        self,
        *,
        full_name: str,
        email: str,
        phone: str | None,
        password_hash: str,
        role: str,
        is_active: bool = True,
    ):
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role,
            is_active=is_active,
        )

        return self.add(user)

    def agents(self):
        return (
            self.db.query(User)
            .filter(
                User.role == "support_agent",
                User.is_active.is_(True),
            )
            .all()
        )