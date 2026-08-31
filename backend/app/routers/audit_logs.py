from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import require_roles
from app.models.audit import AuditLog
from app.schemas.audit import AuditOut
r=APIRouter(prefix="/audit-logs",tags=["Audit Logs"])
@r.get("",response_model=list[AuditOut])
def logs(page:int=1,limit:int=50,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset((page-1)*limit).limit(limit).all()
@r.get("/{id}",response_model=AuditOut)
def get(id:int,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 x=db.get(AuditLog,id)
 if not x:raise HTTPException(404,"Audit log not found")
 return x
