import os,uuid
from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.models.ticket import Ticket
from app.models.attachment import TicketAttachment
r=APIRouter(tags=["Attachments"])
ALLOWED={"pdf","jpg","jpeg","png","doc","docx","txt"}
@r.post("/tickets/{ticket_id}/attachments")
async def upload(ticket_id:int,file:UploadFile=File(...),db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,ticket_id)
 if not t:raise HTTPException(404,"Ticket not found")
 if t.status in ("closed","cancelled"):raise HTTPException(400,"Ticket cannot accept attachments")
 if u.role=="customer" and t.customer.user_id!=u.id:raise HTTPException(403,"Forbidden")
 if u.role=="support_agent" and t.assigned_agent_id!=u.id:raise HTTPException(403,"Forbidden")
 ext=file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else ''
 if ext not in ALLOWED:raise HTTPException(400,"Unsupported file type")
 data=await file.read();max_bytes=settings.max_upload_size_mb*1024*1024
 if len(data)>max_bytes:raise HTTPException(413,f"File exceeds {settings.max_upload_size_mb} MB")
 os.makedirs(settings.upload_dir,exist_ok=True);safe=f"{uuid.uuid4().hex}.{ext}";path=os.path.join(settings.upload_dir,safe)
 with open(path,'wb') as f:f.write(data)
 a=TicketAttachment(ticket_id=ticket_id,uploaded_by_id=u.id,file_name=file.filename,file_path=path,file_size=len(data),file_type=file.content_type or ext);db.add(a);db.commit();db.refresh(a)
 return {"id":a.id,"file_name":a.file_name,"file_size":a.file_size,"file_type":a.file_type,"uploaded_at":a.uploaded_at}
@r.get("/tickets/{ticket_id}/attachments")
def list_files(ticket_id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 t=db.get(Ticket,ticket_id)
 if not t:raise HTTPException(404,"Ticket not found")
 if u.role=="customer" and t.customer.user_id!=u.id:raise HTTPException(403,"Forbidden")
 if u.role=="support_agent" and t.assigned_agent_id!=u.id:raise HTTPException(403,"Forbidden")
 return db.query(TicketAttachment).filter_by(ticket_id=ticket_id).all()
@r.get("/attachments/{id}")
def get_file(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 a=db.get(TicketAttachment,id)
 if not a:raise HTTPException(404,"Attachment not found")
 return {"id":a.id,"file_name":a.file_name,"file_path":a.file_path,"file_size":a.file_size,"file_type":a.file_type}
@r.delete("/attachments/{id}")
def delete(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
 a=db.get(TicketAttachment,id)
 if not a:raise HTTPException(404,"Attachment not found")
 if a.uploaded_by_id!=u.id and u.role!="admin":raise HTTPException(403,"Forbidden")
 if os.path.exists(a.file_path):os.remove(a.file_path)
 db.delete(a);db.commit();return {"message":"Attachment deleted"}
