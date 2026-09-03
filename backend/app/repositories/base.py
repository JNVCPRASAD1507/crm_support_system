
from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, obj):
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def get(self, model, object_id):
        return (
            self.db.query(model)
            .filter(model.id == object_id)
            .first()
        )

    def delete(self, obj):
        self.db.delete(obj)
        self.db.flush()