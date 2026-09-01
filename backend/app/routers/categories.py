from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

from app.services.category_service import CategoryService

from app.core.dependencies import (
    get_current_user,
    require_roles,
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# ============================================================
# CREATE CATEGORY
# ADMIN ONLY
# ============================================================

@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    ),
):

    service = CategoryService(db)

    category = service.create(data)

    db.commit()
    db.refresh(category)

    return category


# ============================================================
# LIST CATEGORIES
# ADMIN / SUPPORT AGENT / CUSTOMER
# ============================================================

@router.get(
    "",
    response_model=list[CategoryResponse],
)
def list_categories(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = CategoryService(db)

    categories, total = service.list(
        skip=skip,
        limit=limit,
        active_only=active_only,
    )

    return categories


# ============================================================
# GET CATEGORY
# ADMIN / SUPPORT AGENT / CUSTOMER
# ============================================================

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = CategoryService(db)

    return service.get(category_id)


# ============================================================
# UPDATE CATEGORY
# ADMIN ONLY
# ============================================================

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    ),
):

    service = CategoryService(db)

    category = service.update(
        category_id,
        data,
    )

    db.commit()
    db.refresh(category)

    return category


# ============================================================
# DELETE CATEGORY
# ADMIN ONLY
# ============================================================

@router.delete(
    "/{category_id}",
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    ),
):

    service = CategoryService(db)

    result = service.delete(
        category_id
    )

    db.commit()

    return result