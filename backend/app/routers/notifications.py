from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.notification import Notification
from app.schemas.notification import NotificationOut
r=APIRouter(prefix="/notifications",tags=["Notifications"])
@r.get("",response_model=list[NotificationOut])
def list(db:Session=Depends(get_db),u=Depends(get_current_user)):return db.query(Notification).filter_by(user_id=u.id).order_by(Notification.created_at.desc()).limit(100).all()
@r.put("/{id}/read")
def read(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 n=db.get(Notification,id)
 if not n or n.user_id!=u.id:raise HTTPException(404,"Notification not found")
 n.is_read=True;db.commit();return {"message":"Marked as read"}
@r.put("/read-all")
def read_all(db:Session=Depends(get_db),u=Depends(get_current_user)):db.query(Notification).filter_by(user_id=u.id,is_read=False).update({"is_read":True});db.commit();return {"message":"All notifications marked as read"}
