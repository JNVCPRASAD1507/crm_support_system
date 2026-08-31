from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.core.dependencies import get_current_user,require_roles
from app.models.ticket import Ticket
from app.models.customer import Customer
from app.models.user import User
from app.services.sla_service import sla_status
r=APIRouter(prefix="/dashboard",tags=["Dashboard"])
def stats(q):
 items=q.all();return {"total_tickets":len(items),"open_tickets":sum(t.status=="open" for t in items),"in_progress_tickets":sum(t.status=="in_progress" for t in items),"waiting_tickets":sum(t.status=="waiting_for_customer" for t in items),"resolved_tickets":sum(t.status=="resolved" for t in items),"closed_tickets":sum(t.status=="closed" for t in items),"critical_tickets":sum(t.priority=="critical" for t in items),"sla_breached_tickets":sum(sla_status(t)=="breached" for t in items)}
@r.get("/admin")
def admin(db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 d=stats(db.query(Ticket));d.update({"total_customers":db.query(Customer).count(),"total_support_agents":db.query(User).filter(User.role=="support_agent").count()});return d
@r.get("/agent")
def agent(db:Session=Depends(get_db),u=Depends(require_roles("support_agent"))):return stats(db.query(Ticket).filter(Ticket.assigned_agent_id==u.id))
@r.get("/customer")
def customer(db:Session=Depends(get_db),u=Depends(require_roles("customer"))):
 q=db.query(Ticket).join(Ticket.customer).filter(Customer.user_id==u.id);d=stats(q);d["recent_tickets"]=q.order_by(Ticket.created_at.desc()).limit(5).all();return d
