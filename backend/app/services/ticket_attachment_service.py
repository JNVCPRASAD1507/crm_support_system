
import os
import uuid
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.ticket_attachment_repository import (
    TicketAttachmentRepository,
)


class TicketAttachmentService:

    # 10 MB maximum per file
    MAX_FILE_SIZE = 10 * 1024 * 1024

    ALLOWED_FILE_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/pdf",
        "text/plain",
        "application/zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf",
        ".txt",
        ".zip",
        ".docx",
        ".xlsx",
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = TicketAttachmentRepository(db)

        self.upload_root = Path("uploads") / "tickets"
        self.upload_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ============================================================
    # ACCESS CONTROL
    # ============================================================

    @staticmethod
    def _can_access_ticket(
        ticket: Ticket,
        user: User,
    ) -> bool:

        if user.role == "admin":
            return True

        if user.role == "support_agent":
            return ticket.assigned_agent_id == user.id

        if user.role == "customer":
            return (
                ticket.customer is not None
                and ticket.customer.user_id == user.id
            )

        return False

    # ============================================================
    # GET TICKET
    # ============================================================

    def _get_ticket_or_404(
        self,
        ticket_id: int,
    ) -> Ticket:

        ticket = self.db.get(
            Ticket,
            ticket_id,
        )

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        return ticket

    # ============================================================
    # CREATE ATTACHMENT
    # ============================================================

    async def create_attachment(
        self,
        ticket_id: int,
        current_user: User,
        upload_file,
    ):

        ticket = self._get_ticket_or_404(ticket_id)

        if not self._can_access_ticket(
            ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        if ticket.status in {
            "closed",
            "cancelled",
        }:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Attachments cannot be added to a "
                    "closed or cancelled ticket"
                ),
            )

        original_name = Path(
            upload_file.filename or ""
        ).name

        if not original_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file name",
            )

        extension = Path(
            original_name
        ).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "File type is not allowed"
                ),
            )

        content_type = (
            upload_file.content_type
            or "application/octet-stream"
        )

        if content_type not in self.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "File MIME type is not allowed"
                ),
            )

        # --------------------------------------------------------
        # Read file
        # --------------------------------------------------------

        content = await upload_file.read()

        file_size = len(content)

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File cannot be empty",
            )

        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Maximum file size is 10 MB",
            )

        # --------------------------------------------------------
        # Generate secure storage name
        # --------------------------------------------------------

        stored_name = (
            f"{uuid.uuid4().hex}{extension}"
        )

        ticket_directory = (
            self.upload_root / str(ticket_id)
        )

        ticket_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            ticket_directory / stored_name
        )

        file_path.write_bytes(content)

        # --------------------------------------------------------
        # Save DB record
        # --------------------------------------------------------

        attachment = self.repository.create(
            ticket_id=ticket_id,
            uploaded_by_id=current_user.id,
            file_name=original_name,
            file_path=str(file_path),
            file_size=file_size,
            file_type=content_type,
        )

        return attachment

    # ============================================================
    # LIST
    # ============================================================

    def get_ticket_attachments(
        self,
        ticket_id: int,
        current_user: User,
    ):

        ticket = self._get_ticket_or_404(ticket_id)

        if not self._can_access_ticket(
            ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this ticket",
            )

        return self.repository.get_by_ticket(
            ticket_id
        )

    # ============================================================
    # GET SINGLE
    # ============================================================

    def get_attachment(
        self,
        attachment_id: int,
        current_user: User,
    ):

        attachment = self.repository.get_by_id(
            attachment_id
        )

        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found",
            )

        if not self._can_access_ticket(
            attachment.ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this attachment",
            )

        return attachment

    # ============================================================
    # DELETE
    # ============================================================

    def delete_attachment(
        self,
        attachment_id: int,
        current_user: User,
    ):

        attachment = self.repository.get_by_id(
            attachment_id
        )

        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found",
            )

        if not self._can_access_ticket(
            attachment.ticket,
            current_user,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this attachment",
            )

        # Admin can delete any attachment.
        # Other users can delete only their own attachment.
        if (
            current_user.role != "admin"
            and attachment.uploaded_by_id
            != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You can only delete your own attachments"
                ),
            )

        file_path = Path(
            attachment.file_path
        )

        if file_path.exists():
            file_path.unlink()

        self.repository.delete(
            attachment
        )

        self.db.commit()

        return {
            "message": "Attachment deleted successfully"
        }
