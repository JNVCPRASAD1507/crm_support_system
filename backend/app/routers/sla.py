from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from app.db.session import get_db
from app.core.dependencies import require_roles,get_current_user
from app.models.ticket import Ticket
from app.services.sla_service import sla_status
r=APIRouter(prefix="/sla",tags=["SLA"])
def rows(q):return [{"ticket_id":t.id,"subject":t.subject,"priority":t.priority,"status":t.status,"sla_deadline":t.sla_deadline,"sla_status":sla_status(t)} for t in q]
@r.get("/tickets")
def tickets(db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):return rows(db.query(Ticket).filter(Ticket.status.notin_(["closed","cancelled"])).all())
@r.get("/breached")
def breached(db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):return [x for x in rows(db.query(Ticket).filter(Ticket.status.notin_(["closed","cancelled"])).all()) if x["sla_status"]=="breached"]
@r.get("/at-risk")
def risk(db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):return [x for x in rows(db.query(Ticket).filter(Ticket.status.notin_(["closed","cancelled"])).all()) if x["sla_status"]=="at_risk"]
