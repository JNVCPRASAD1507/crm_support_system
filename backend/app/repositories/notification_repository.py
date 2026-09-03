
from sqlalchemy.orm import Session

from app.models.notification import Notification
from .base import BaseRepository


class NotificationRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        *,
        user_id: int,
        ticket_id: int | None,
        notification_type: str,
        title: str,
        message: str,
    ) -> Notification:

        notification = Notification(
            user_id=user_id,
            ticket_id=ticket_id,
            type=notification_type,
            title=title,
            message=message,
            is_read=False,
        )

        return self.add(notification)

    def get_by_id(
        self,
        notification_id: int,
    ) -> Notification | None:

        return (
            self.db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def list_for_user(
        self,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ) -> list[Notification]:

        query = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
        )

        if unread_only:
            query = query.filter(
                Notification.is_read.is_(False)
            )

        return (
            query
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def mark_as_read(
        self,
        notification: Notification,
    ) -> Notification:

        notification.is_read = True

        self.db.commit()
        self.db.refresh(notification)

        return notification

    def mark_all_as_read(
        self,
        user_id: int,
    ) -> int:

        notifications = (
            self.db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .all()
        )

        for notification in notifications:
            notification.is_read = True

        self.db.commit()

        return len(notifications)
