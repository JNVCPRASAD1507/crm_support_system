from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user,require_roles
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import *
from app.services.ticket_service import TicketService
from app.services.audit_service import AuditService
r=APIRouter(prefix="/tickets",tags=["Tickets"])
@r.post("",response_model=TicketOut,status_code=201)
def create(data:TicketCreate,db:Session=Depends(get_db),u=Depends(get_current_user)):
 if u.role not in ("customer","admin","support_agent"):raise HTTPException(403,"Forbidden")
 t=TicketService.create(db,data.model_dump(),u);db.commit();db.refresh(t);return t
@r.get("",response_model=dict)
def list_tickets(search:str|None=None,status:str|None=None,priority:str|None=None,category_id:int|None=None,assigned_agent_id:int|None=None,page:int=1,limit:int=20,db:Session=Depends(get_db),u=Depends(get_current_user)):
 q=db.query(Ticket)
 if u.role=="customer":q=q.join(Ticket.customer).filter(__import__('app.models.customer',fromlist=['Customer']).Customer.user_id==u.id)
 elif u.role=="support_agent":q=q.filter(Ticket.assigned_agent_id==u.id)
 if search:q=q.filter((Ticket.subject.ilike(f"%{search}%"))|(Ticket.description.ilike(f"%{search}%")))
 for k,v in [("status",status),("priority",priority),("category_id",category_id),("assigned_agent_id",assigned_agent_id)]:
  if v is not None:q=q.filter(getattr(Ticket,k)==v)
 total=q.count();items=q.order_by(Ticket.created_at.desc()).offset((page-1)*limit).limit(limit).all();return {"items":items,"page":page,"limit":limit,"total":total}
@r.get("/unassigned")
def unassigned(db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):return db.query(Ticket).filter(Ticket.assigned_agent_id==None,Ticket.status.notin_(["closed","cancelled"])).all()
@r.get("/workload")
def workload(db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 agents=db.query(User).filter(User.role=="support_agent").all();return [{"agent_id":a.id,"name":a.full_name,"active":a.is_active,"open_tickets":db.query(Ticket).filter(Ticket.assigned_agent_id==a.id,Ticket.status.in_(["open","in_progress","waiting_for_customer"])).count()} for a in agents]
@r.get("/{id}",response_model=TicketOut)
def get(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,id)
 if not t:raise HTTPException(404,"Ticket not found")
 TicketService.ensure_access(t,u);return t
@r.put("/{id}",response_model=TicketOut)
def update(id:int,data:TicketUpdate,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,id)
 if not t:raise HTTPException(404,"Ticket not found")
 TicketService.ensure_access(t,u,True)
 if data.status:return TicketService.transition(db,t,data.status,u)
 for k,v in data.model_dump(exclude_none=True).items():setattr(t,k,v)
 AuditService.log(db,u.id,"ticket_updated","ticket",id);db.commit();db.refresh(t);return t
@r.put("/{id}/assign",response_model=TicketOut)
def assign(id:int,data:AssignIn,db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):
 t=db.get(Ticket,id);a=db.get(User,data.agent_id)
 if not t:raise HTTPException(404,"Ticket not found")
 if not a or a.role!="support_agent" or not a.is_active:raise HTTPException(400,"Cannot assign to inactive/non-agent user")
 if u.role=="support_agent" and t.assigned_agent_id!=u.id:raise HTTPException(403,"Only assigned agent can reassign this ticket")
 old=t.assigned_agent_id;t.assigned_agent_id=a.id;AuditService.log(db,u.id,"ticket_assigned","ticket",id,{"agent_id":old},{"agent_id":a.id});db.commit();db.refresh(t);return t
@r.put("/{id}/reassign",response_model=TicketOut)
def reassign(id:int,data:AssignIn,db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):return assign(id,data,db,u)
@r.put("/{id}/resolve",response_model=TicketOut)
def resolve(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,id)
 if not t:raise HTTPException(404,"Ticket not found")
 out=TicketService.transition(db,t,"resolved",u);db.commit();db.refresh(out);return out
@r.put("/{id}/close",response_model=TicketOut)
def close(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,id)
 if not t:raise HTTPException(404,"Ticket not found")
 out=TicketService.transition(db,t,"closed",u);db.commit();db.refresh(out);return out
@r.put("/{id}/cancel",response_model=TicketOut)
def cancel(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,id)
 if not t:raise HTTPException(404,"Ticket not found")
 out=TicketService.transition(db,t,"cancelled",u);db.commit();db.refresh(out);return out
