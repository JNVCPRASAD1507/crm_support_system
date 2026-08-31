from pydantic import BaseModel
from datetime import datetime
from .common import ORM
class NotificationOut(ORM): id:int; user_id:int; title:str; message:str; type:str; is_read:bool; created_at:datetime
