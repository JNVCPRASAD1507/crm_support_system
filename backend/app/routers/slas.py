from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sla import SLACreate, SLAResponse, SLAUpdate
from app.services.sla_service import SLAService


router = APIRouter(
    prefix="/slas",
    tags=["SLA Management"],
)


@router.post(
    "",
    response_model=SLAResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sla(
    data: SLACreate,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    sla = service.create(data)

    db.commit()
    db.refresh(sla)

    return sla


@router.get(
    "",
    response_model=list[SLAResponse],
)
def list_slas(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    return service.list(
        skip=skip,
        limit=limit,
        active_only=active_only,
    )


# ---------------------------------------------------------
# Priority routes
# More specific route MUST come first
# ---------------------------------------------------------

@router.get(
    "/priority/{priority}/deadlines",
)
def calculate_sla_deadlines(
    priority: str,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    return service.calculate_deadlines(priority)


@router.get(
    "/priority/{priority}",
    response_model=SLAResponse,
)
def get_sla_by_priority(
    priority: str,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    return service.get_sla_for_priority(priority)


# ---------------------------------------------------------
# ID routes
# ---------------------------------------------------------

@router.get(
    "/{sla_id}",
    response_model=SLAResponse,
)
def get_sla(
    sla_id: int,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    return service.get_by_id(sla_id)


@router.put(
    "/{sla_id}",
    response_model=SLAResponse,
)
def update_sla(
    sla_id: int,
    data: SLAUpdate,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    sla = service.update(
        sla_id,
        data,
    )

    db.commit()
    db.refresh(sla)

    return sla


@router.delete(
    "/{sla_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_sla(
    sla_id: int,
    db: Session = Depends(get_db),
):
    service = SLAService(db)

    service.delete(sla_id)

    db.commit()

    return None