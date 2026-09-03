from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_log_service import AuditLogService


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def list_audit_logs(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    user_id: int | None = Query(
        default=None,
    ),
    action: str | None = Query(
        default=None,
    ),
    entity_type: str | None = Query(
        default=None,
    ),
    entity_id: int | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
):
    service = AuditLogService(db)

    return service.list(
        skip=skip,
        limit=limit,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
    )


@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
)
def get_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
):
    service = AuditLogService(db)

    audit_log = service.get_by_id(audit_log_id)

    if not audit_log:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found",
        )

    return audit_log

