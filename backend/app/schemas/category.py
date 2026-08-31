from pydantic import BaseModel
from .common import ORM
class CategoryCreate(BaseModel): name:str; description:str|None=None; is_active:bool=True
class CategoryUpdate(BaseModel): name:str|None=None; description:str|None=None; is_active:bool|None=None
class CategoryOut(ORM): id:int; name:str; description:str|None; is_active:bool
