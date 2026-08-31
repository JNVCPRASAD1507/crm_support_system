
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import (
    CustomerCreate,
    CustomerOut,
    CustomerUpdate,
)


r = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@r.get(
    "",
    response_model=list[CustomerOut],
)
def list_customers(
    search: str | None = None,
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    user: User = Depends(
        require_roles("admin", "support_agent")
    ),
):
    query = db.query(Customer)

    if search:
        like = f"%{search.strip()}%"

        query = query.filter(
            (Customer.name.ilike(like))
            | (Customer.email.ilike(like))
            | (Customer.company.ilike(like))
        )

    if status_filter:
        query = query.filter(
            Customer.status == status_filter
        )

    return (
        query
        .order_by(Customer.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@r.get(
    "/me",
    response_model=CustomerOut,
)
def my_customer(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    customer = (
        db.query(Customer)
        .filter(Customer.user_id == user.id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No customer profile linked to this account",
        )

    return customer


@r.get(
    "/{customer_id}",
    response_model=CustomerOut,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(
        require_roles("admin", "support_agent")
    ),
):
    customer = db.get(
        Customer,
        customer_id,
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


@r.post(
    "",
    response_model=CustomerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(
        require_roles("admin", "support_agent")
    ),
):
    customer = Customer(
        name=data.name.strip(),
        email=str(data.email).strip().lower(),
        phone=data.phone,
        company=data.company,
        address=data.address,
        status=data.status,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@r.put(
    "/{customer_id}",
    response_model=CustomerOut,
)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(
        require_roles("admin", "support_agent")
    ),
):
    customer = db.get(
        Customer,
        customer_id,
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    values = data.model_dump(
        exclude_none=True,
    )

    if "name" in values:
        values["name"] = values["name"].strip()

    if "email" in values:
        values["email"] = (
            str(values["email"])
            .strip()
            .lower()
        )

    for key, value in values.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


@r.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(
        require_roles("admin")
    ),
):
    customer = db.get(
        Customer,
        customer_id,
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    db.delete(customer)
    db.commit()

    return None