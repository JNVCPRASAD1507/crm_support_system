from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user,require_roles
from app.models.category import Category
from app.schemas.category import *
r=APIRouter(prefix="/categories",tags=["Categories"])
@r.post("",response_model=CategoryOut,status_code=201)
def create(data:CategoryCreate,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 if db.query(Category).filter(Category.name.ilike(data.name)).first():raise HTTPException(409,"Duplicate category name")
 c=Category(**data.model_dump());db.add(c);db.commit();db.refresh(c);return c
@r.get("",response_model=list[CategoryOut])
def list(search:str|None=None,db:Session=Depends(get_db),u=Depends(get_current_user)):q=db.query(Category);return q.filter(Category.name.ilike(f"%{search}%")).all() if search else q.all()
@r.get("/{id}",response_model=CategoryOut)
def get(id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):return db.get(Category,id)
@r.put("/{id}",response_model=CategoryOut)
def update(id:int,data:CategoryUpdate,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 c=db.get(Category,id)
 if not c:raise HTTPException(404,"Category not found")
 if data.name and db.query(Category).filter(Category.name.ilike(data.name),Category.id!=id).first():raise HTTPException(409,"Duplicate category name")
 for k,v in data.model_dump(exclude_none=True).items():setattr(c,k,v)
 db.commit();db.refresh(c);return c
@r.delete("/{id}")
def delete(id:int,db:Session=Depends(get_db),u=Depends(require_roles("admin"))):
 c=db.get(Category,id)
 if not c:raise HTTPException(404,"Category not found")
 db.delete(c);db.commit();return {"message":"Category deleted"}
