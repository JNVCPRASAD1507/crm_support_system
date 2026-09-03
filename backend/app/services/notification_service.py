from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories.notification_repository import (
    NotificationRepository,
)


class NotificationService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = NotificationRepository(db)

    # ============================================================
    # CREATE NOTIFICATION
    # ============================================================

    def create(
        self,
        *,
        user_id: int,
        ticket_id: int | None,
        notification_type: str,
        title: str,
        message: str,
    ) -> Notification:

        return self.repository.create(
            user_id=user_id,
            ticket_id=ticket_id,
            notification_type=notification_type,
            title=title,
            message=message,
        )

    # ============================================================
    # GET USER NOTIFICATIONS
    # ============================================================

    def list(
        self,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ):

        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="skip cannot be negative",
            )

        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit must be between 1 and 100",
            )

        return self.repository.list_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            unread_only=unread_only,
        )

    # ============================================================
    # MARK ONE AS READ
    # ============================================================

    def mark_as_read(
        self,
        *,
        notification_id: int,
        user_id: int,
    ):

        notification = self.repository.get_by_id(
            notification_id
        )

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )

        if notification.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot modify this notification",
            )

        if notification.is_read:
            return notification

        return self.repository.mark_as_read(notification)

    # ============================================================
    # MARK ALL AS READ
    # ============================================================

    def mark_all_as_read(
        self,
        *,
        user_id: int,
    ):

        count = self.repository.mark_all_as_read(
            user_id
        )

        return {
            "message": "All notifications marked as read",
            "updated_count": count,
        }
        
        
        