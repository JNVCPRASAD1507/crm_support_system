from app.models.category import Category

from .base import BaseRepository


class CategoryRepository(BaseRepository):

    def get_by_id(self, category_id: int):
        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def get_by_name(self, name: str):
        return (
            self.db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = False,
    ):
        query = self.db.query(Category)

        if active_only:
            query = query.filter(
                Category.is_active.is_(True)
            )

        total = query.count()

        items = (
            query
            .order_by(Category.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    def create(
        self,
        *,
        name: str,
        description: str | None,
        is_active: bool,
    ):
        category = Category(
            name=name,
            description=description,
            is_active=is_active,
        )

        return self.add(category)

    def update(
        self,
        category: Category,
        *,
        name: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ):
        if name is not None:
            category.name = name

        if description is not None:
            category.description = description

        if is_active is not None:
            category.is_active = is_active

        self.db.flush()
        self.db.refresh(category)

        return category

    def delete(self, category: Category):
        self.db.delete(category)
        self.db.flush()