from pydantic import BaseModel
from datetime import datetime
from .common import ORM
class AuditOut(ORM): id:int; user_id:int|None; action:str; entity:str; entity_id:int; previous_value:str|None; new_value:str|None; timestamp:datetime
