from pydantic import BaseModel,Field
from datetime import datetime
from .common import ORM
class TicketCreate(BaseModel): customer_id:int|None=None; subject:str=Field(min_length=3,max_length=200); description:str=Field(min_length=3); category_id:int|None=None; priority:str="medium"
class TicketUpdate(BaseModel): subject:str|None=None; description:str|None=None; category_id:int|None=None; priority:str|None=None; status:str|None=None
class AssignIn(BaseModel): agent_id:int
class TicketOut(ORM): id:int; customer_id:int; assigned_agent_id:int|None; category_id:int|None; subject:str; description:str; priority:str; status:str; created_at:datetime; updated_at:datetime|None; resolved_at:datetime|None; sla_deadline:datetime|None; first_response_at:datetime|None
