from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user,require_roles
from app.models.customer import Customer
from app.schemas.customer import *
from app.services.audit_service import AuditService
r=APIRouter(prefix="/customers",tags=["Customers"])
@r.post("",response_model=CustomerOut,status_code=201)
def create(data:CustomerCreate,db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):
 c=Customer(**data.model_dump());db.add(c);db.flush();AuditService.log(db,u.id,"customer_created","customer",c.id,new=data.model_dump());db.commit();db.refresh(c);return c
@r.get("",response_model=dict)
def list_customers(search:str|None=None,status:str|None=None,page:int=1,limit:int=20,db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):
 q=db.query(Customer)
 if search:q=q.filter((Customer.name.ilike(f"%{search}%"))|(Customer.email.ilike(f"%{search}%"))|(Customer.company.ilike(f"%{search}%")))
 if status:q=q.filter(Customer.status==status)
 total=q.count();items=q.offset((page-1)*limit).limit(limit).all();return {"items":items,"page":page,"limit":limit,"total":total}
@r.get("/{id}",response_model=CustomerOut)
def get(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 c=db.get(Customer,id)
 if not c:raise HTTPException(404,"Customer not found")
 if u.role=="customer" and c.user_id!=u.id:raise HTTPException(403,"Forbidden")
 return c
@r.put("/{id}",response_model=CustomerOut)
def update(id:int,data:CustomerUpdate,db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):
 c=db.get(Customer,id)
 if not c:raise HTTPException(404,"Customer not found")
 old={k:getattr(c,k) for k in data.model_dump(exclude_none=True)}
 for k,v in data.model_dump(exclude_none=True).items():setattr(c,k,v)
 AuditService.log(db,u.id,"customer_updated","customer",id,old,data.model_dump(exclude_none=True));db.commit();db.refresh(c);return c
@r.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 c=db.get(Customer,id)
 if not c:raise HTTPException(404,"Customer not found")
 db.delete(c);db.commit();return {"message":"Customer deleted"}
@r.get("/{id}/tickets")
def history(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 c=db.get(Customer,id)
 if not c:raise HTTPException(404,"Customer not found")
 if u.role=="customer" and c.user_id!=u.id:raise HTTPException(403,"Forbidden")
 return c.tickets
