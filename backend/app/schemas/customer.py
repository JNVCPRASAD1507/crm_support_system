from pydantic import BaseModel,EmailStr
from datetime import datetime
from .common import ORM
class CustomerCreate(BaseModel): name:str; email:EmailStr; phone:str|None=None; company:str|None=None; address:str|None=None; status:str="active"; user_id:int|None=None
class CustomerUpdate(BaseModel): name:str|None=None; email:EmailStr|None=None; phone:str|None=None; company:str|None=None; address:str|None=None; status:str|None=None
class CustomerOut(ORM): id:int; name:str; email:EmailStr; phone:str|None; company:str|None; address:str|None; status:str; created_at:datetime
