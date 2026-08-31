from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import require_roles
from app.core.security import hash_password
from app.models.user import User
r=APIRouter(prefix="/users",tags=["User Management"])
@r.get("/agents")
def agents(db:Session=Depends(get_db),u=Depends(require_roles("admin","support_agent"))):return db.query(User).filter(User.role=="support_agent").all()
@r.post("/agents")
def create_agent(data:dict,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 if db.query(User).filter(User.email==data.get("email")).first():raise HTTPException(409,"Email already exists")
 x=User(full_name=data.get("full_name"),email=data.get("email"),phone=data.get("phone"),password_hash=hash_password(data.get("password","Agent@123")),role="support_agent",is_active=True);db.add(x);db.commit();db.refresh(x);return x
@r.put("/{id}/toggle-active")
def toggle(id:int,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 x=db.get(User,id)
 if not x:raise HTTPException(404,"User not found")
 x.is_active=not x.is_active;db.commit();return {"id":x.id,"is_active":x.is_active}
