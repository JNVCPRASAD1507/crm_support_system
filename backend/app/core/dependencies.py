from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User
oauth2=OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token:str=Depends(oauth2),db:Session=Depends(get_db)):
    data=decode_token(token)
    if not data or not data.get("sub"): raise HTTPException(status_code=401,detail="Invalid or expired token")
    user=db.get(User,int(data["sub"]))
    if not user or not user.is_active: raise HTTPException(status_code=401,detail="Inactive or missing user")
    return user
def require_roles(*roles):
    def dep(user=Depends(get_current_user)):
        if user.role not in roles: raise HTTPException(status_code=403,detail="Insufficient role")
        return user
    return dep
