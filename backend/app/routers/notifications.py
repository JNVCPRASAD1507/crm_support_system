from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.notification import NotificationResponse
from app.services.notification_service import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# ============================================================
# GET NOTIFICATIONS
# ============================================================

@router.get(
    "",
    response_model=list[NotificationResponse],
)
def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = False,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = NotificationService(db)

    return service.list(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
    )


# ============================================================
# MARK ONE AS READ
# ============================================================

@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_as_read(
    notification_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = NotificationService(db)

    return service.mark_as_read(
        notification_id=notification_id,
        user_id=current_user.id,
    )


# ============================================================
# MARK ALL AS READ
# ============================================================

@router.put("/read-all")
def mark_all_notifications_as_read(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = NotificationService(db)

    return service.mark_all_as_read(
        user_id=current_user.id,
    )
    
    