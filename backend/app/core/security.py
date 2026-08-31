from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(p): return pwd_context.hash(p)
def verify_password(p,h): return pwd_context.verify(p,h)
def create_access_token(subject):
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":str(subject),"exp":exp},settings.secret_key,algorithm=settings.algorithm)
def decode_token(token):
    try: return jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
    except JWTError: return None
