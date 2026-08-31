from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, model, id):
        return self.db.get(model, id)

    def add(self, obj):
        self.db.add(obj)
        self.db.flush()
        return obj

    def delete(self, obj):
        self.db.delete(obj)
        self.db.flush()
