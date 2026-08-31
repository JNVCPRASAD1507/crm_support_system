from pydantic import BaseModel, ConfigDict
from datetime import datetime
class ORM(BaseModel): model_config=ConfigDict(from_attributes=True)
class Page(BaseModel): items:list; page:int; limit:int; total:int
