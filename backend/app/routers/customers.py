from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut

r = APIRouter(prefix="/customers", tags=["Customers"])


@r.get("", response_model=list[CustomerOut])
def list_customers(
    search: str | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "support_agent")),
):
    q = db.query(Customer)
    if search:
        like = f"%{search}%"
        q = q.filter(
            (Customer.name.ilike(like))
            | (Customer.email.ilike(like))
            | (Customer.company.ilike(like))
        )
    if status:
        q = q.filter(Customer.status == status)
    return q.offset(skip).limit(limit).all()


@r.get("/me", response_model=CustomerOut)
def my_customer(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    c = db.query(Customer).filter(Customer.user_id == user.id).first()
    if not c:
        raise HTTPException(404, "No customer profile linked to this account")
    return c


@r.get("/{customer_id}", response_model=CustomerOut)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "support_agent")),
):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(404, "Customer not found")
    return c


@r.post("", response_model=CustomerOut, status_code=201)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "support_agent")),
):
    c = Customer(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@r.put("/{customer_id}", response_model=CustomerOut)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "support_agent")),
):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(404, "Customer not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c


@r.delete("/{customer_id}", status_code=204)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin")),
):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(404, "Customer not found")
    db.delete(c)
    db.commit()