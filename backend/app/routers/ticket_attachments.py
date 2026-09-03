
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ticket_attachment import (
    TicketAttachmentResponse,
)
from app.services.ticket_attachment_service import (
    TicketAttachmentService,
)


router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Attachments"],
)


# ============================================================
# UPLOAD
# ============================================================

@router.post(
    "/{ticket_id}/attachments",
    response_model=TicketAttachmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_attachment(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = TicketAttachmentService(db)

    attachment = await service.create_attachment(
        ticket_id=ticket_id,
        current_user=current_user,
        upload_file=file,
    )

    db.commit()
    db.refresh(attachment)

    return attachment


# ============================================================
# LIST
# ============================================================

@router.get(
    "/{ticket_id}/attachments",
    response_model=list[TicketAttachmentResponse],
)
def list_attachments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = TicketAttachmentService(db)

    return service.get_ticket_attachments(
        ticket_id=ticket_id,
        current_user=current_user,
    )


# ============================================================
# DOWNLOAD
# ============================================================

@router.get(
    "/attachments/{attachment_id}/download",
)
def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = TicketAttachmentService(db)

    attachment = service.get_attachment(
        attachment_id=attachment_id,
        current_user=current_user,
    )

    return FileResponse(
        path=attachment.file_path,
        filename=attachment.file_name,
        media_type=attachment.file_type,
    )


# ============================================================
# DELETE
# ============================================================

@router.delete(
    "/attachments/{attachment_id}",
)
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = TicketAttachmentService(db)

    return service.delete_attachment(
        attachment_id=attachment_id,
        current_user=current_user,
    )
