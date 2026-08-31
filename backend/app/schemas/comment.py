from pydantic import BaseModel,Field
from datetime import datetime
from .common import ORM
class CommentCreate(BaseModel): comment:str=Field(min_length=1,max_length=5000)
class CommentUpdate(BaseModel): comment:str=Field(min_length=1,max_length=5000)
class CommentOut(ORM): id:int; ticket_id:int; user_id:int; comment:str; created_at:datetime; updated_at:datetime|None
