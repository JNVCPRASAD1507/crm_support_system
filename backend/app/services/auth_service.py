from fastapi import HTTPException
from app.core.security import hash_password,verify_password,create_access_token
from app.models.user import User
from app.models.customer import Customer
class AuthService:
 @staticmethod
 def register(db,data):
  if db.query(User).filter(User.email==data.email).first():raise HTTPException(409,"Email already registered")
  u=User(full_name=data.full_name,email=data.email,phone=data.phone,password_hash=hash_password(data.password),role="customer",is_active=True);db.add(u);db.flush();db.add(Customer(user_id=u.id,name=data.full_name,email=data.email,phone=data.phone,status="active"));return u
 @staticmethod
 def login(db,email,password):
  u=db.query(User).filter(User.email==email).first()
  if not u or not verify_password(password,u.password_hash):raise HTTPException(401,"Invalid email or password")
  if not u.is_active:raise HTTPException(403,"Account inactive")
  return create_access_token(u.id),u
