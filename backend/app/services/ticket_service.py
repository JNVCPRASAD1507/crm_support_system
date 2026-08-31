from datetime import datetime,timezone
from fastapi import HTTPException
from app.models.ticket import Ticket
from app.models.user import User
from app.services.sla_service import deadline
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService
TRANS={"open":{"in_progress","cancelled"},"in_progress":{"waiting_for_customer","resolved","cancelled"},"waiting_for_customer":{"in_progress","cancelled"},"resolved":{"closed"},"closed":set(),"cancelled":set()}
class TicketService:
    @staticmethod
    def ensure_access(ticket,user,write=False):
        if user.role=="admin":return
        if user.role=="customer":
            if not ticket.customer or ticket.customer.user_id!=user.id: raise HTTPException(403,"You can only access your own tickets")
            if write and ticket.status in ("closed","cancelled"): raise HTTPException(400,"Ticket cannot be modified")
        elif user.role=="support_agent":
            if ticket.assigned_agent_id!=user.id: raise HTTPException(403,"Ticket is not assigned to you")
            if write and ticket.status in ("closed","cancelled"): raise HTTPException(400,"Ticket cannot be modified")
    @staticmethod
    def create(db,data,user):
        customer_id=user.customer.id if user.role=="customer" and user.customer else data.get("customer_id")
        if not customer_id: raise HTTPException(400,"Customer profile is required")
        t=Ticket(customer_id=customer_id,subject=data["subject"],description=data["description"],category_id=data.get("category_id"),priority=data.get("priority","medium"),sla_deadline=deadline(db,data.get("priority","medium")))
        db.add(t);db.flush(); AuditService.log(db,user.id,"ticket_created","ticket",t.id,new={"subject":t.subject}); NotificationService.notify(db,[user.id],"Ticket created",f"Ticket #{t.id} was created","ticket"); return t
    @staticmethod
    def transition(db,ticket,new_status,user):
        TicketService.ensure_access(ticket,user,True)
        old=ticket.status
        if new_status==old:return ticket
        if new_status not in TRANS.get(old,set()): raise HTTPException(400,f"Invalid status transition: {old} -> {new_status}")
        ticket.status=new_status
        if new_status=="resolved":ticket.resolved_at=datetime.now(timezone.utc)
        AuditService.log(db,user.id,"ticket_status_changed","ticket",ticket.id,previous={"status":old},new={"status":new_status}); NotificationService.notify(db,[ticket.customer.user_id if ticket.customer else None,ticket.assigned_agent_id],"Ticket status changed",f"Ticket #{ticket.id}: {old} → {new_status}","status"); return ticket
