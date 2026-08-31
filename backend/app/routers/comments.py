from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.ticket import Ticket
from app.models.comment import TicketComment
from app.schemas.comment import *
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService
r=APIRouter(tags=["Comments"])
@r.post("/tickets/{ticket_id}/comments",response_model=CommentOut,status_code=201)
def add(ticket_id:int,data:CommentCreate,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,ticket_id)
 if not t:raise HTTPException(404,"Ticket not found")
 if t.status=="closed":raise HTTPException(400,"Closed tickets do not accept comments")
 if u.role=="customer" and t.customer.user_id!=u.id:raise HTTPException(403,"Forbidden")
 if u.role=="support_agent" and t.assigned_agent_id!=u.id:raise HTTPException(403,"Ticket is not assigned to you")
 c=TicketComment(ticket_id=ticket_id,user_id=u.id,comment=data.comment);db.add(c);db.flush();AuditService.log(db,u.id,"comment_added","ticket_comment",c.id,new={"ticket_id":ticket_id});NotificationService.notify(db,[t.customer.user_id,t.assigned_agent_id],"New ticket comment",f"New comment on ticket #{ticket_id}");db.commit();db.refresh(c);return c
@r.get("/tickets/{ticket_id}/comments",response_model=list[CommentOut])
def list_comments(ticket_id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,ticket_id)
 if not t:raise HTTPException(404,"Ticket not found")
 if u.role=="customer" and t.customer.user_id!=u.id:raise HTTPException(403,"Forbidden")
 if u.role=="support_agent" and t.assigned_agent_id!=u.id:raise HTTPException(403,"Forbidden")
 return db.query(TicketComment).filter_by(ticket_id=ticket_id).order_by(TicketComment.created_at).all()
@r.put("/comments/{id}",response_model=CommentOut)
def update(id:int,data:CommentUpdate,db:Session=Depends(get_db),u=Depends(get_current_user)):
 c=db.get(TicketComment,id)
 if not c:raise HTTPException(404,"Comment not found")
 if c.ticket.status=="closed":raise HTTPException(400,"Closed tickets cannot be modified")
 if c.user_id!=u.id and u.role!="admin":raise HTTPException(403,"You can only edit your own comment")
 if u.role=="customer" and c.user.role=="support_agent":raise HTTPException(403,"Customers cannot modify agent comments")
 c.comment=data.comment;db.commit();db.refresh(c);return c
@r.delete("/comments/{id}")
def delete(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 c=db.get(TicketComment,id)
 if not c:raise HTTPException(404,"Comment not found")
 if c.user_id!=u.id and u.role!="admin":raise HTTPException(403,"Forbidden")
 AuditService.log(db,u.id,"comment_deleted","ticket_comment",id);db.delete(c);db.commit();return {"message":"Comment deleted"}
