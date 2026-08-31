import json
from app.models.audit import AuditLog
class AuditService:
    @staticmethod
    def log(db,user_id,action,entity,entity_id,previous=None,new=None):
        db.add(AuditLog(user_id=user_id,action=action,entity=entity,entity_id=entity_id,previous_value=json.dumps(previous,default=str) if previous is not None else None,new_value=json.dumps(new,default=str) if new is not None else None))
