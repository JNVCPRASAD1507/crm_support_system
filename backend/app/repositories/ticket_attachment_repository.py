
from sqlalchemy.orm import Session

from app.models.ticket_attachment import TicketAttachment
from app.repositories.base import BaseRepository


class TicketAttachmentRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    # ============================================================
    # CREATE
    # ============================================================

    def create(
        self,
        ticket_id: int,
        uploaded_by_id: int,
        file_name: str,
        file_path: str,
        file_size: int,
        file_type: str,
    ) -> TicketAttachment:

        attachment = TicketAttachment(
            ticket_id=ticket_id,
            uploaded_by_id=uploaded_by_id,
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
        )

        self.db.add(attachment)
        self.db.flush()

        self.db.refresh(attachment)

        return attachment

    # ============================================================
    # GET BY ID
    # ============================================================

    def get_by_id(
        self,
        attachment_id: int,
    ) -> TicketAttachment | None:

        return (
            self.db.query(TicketAttachment)
            .filter(
                TicketAttachment.id == attachment_id
            )
            .first()
        )

    # ============================================================
    # GET BY TICKET
    # ============================================================

    def get_by_ticket(
        self,
        ticket_id: int,
    ) -> list[TicketAttachment]:

        return (
            self.db.query(TicketAttachment)
            .filter(
                TicketAttachment.ticket_id == ticket_id
            )
            .order_by(
                TicketAttachment.uploaded_at.asc()
            )
            .all()
        )

    # ============================================================
    # DELETE
    # ============================================================

    def delete(
        self,
        attachment: TicketAttachment,
    ) -> None:

        self.db.delete(attachment)
        self.db.flush()
