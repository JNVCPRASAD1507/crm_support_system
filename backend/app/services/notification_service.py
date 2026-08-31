from app.models.notification import Notification
from app.models.user import User
class NotificationService:
    @staticmethod
    def notify(db,user_ids,title,message,type="info"):
        for uid in set(user_ids):
            if uid: db.add(Notification(user_id=uid,title=title,message=message,type=type))
