from fastapi import HTTPException, status

from app.repositories.category_repository import (
    CategoryRepository,
)


class CategoryService:

    def __init__(self, db):
        self.repository = CategoryRepository(db)

    def create(self, data):

        existing = self.repository.get_by_name(
            data.name
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists",
            )

        return self.repository.create(
            name=data.name,
            description=data.description,
            is_active=data.is_active,
        )

    def get(self, category_id: int):

        category = self.repository.get_by_id(
            category_id
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return category

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = False,
    ):

        return self.repository.list(
            skip=skip,
            limit=limit,
            active_only=active_only,
        )

    def update(
        self,
        category_id: int,
        data,
    ):

        category = self.get(category_id)

        if data.name is not None:

            existing = self.repository.get_by_name(
                data.name
            )

            if (
                existing
                and existing.id != category.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category name already exists",
                )

        return self.repository.update(
            category,
            name=data.name,
            description=data.description,
            is_active=data.is_active,
        )

    def delete(self, category_id: int):

        category = self.get(category_id)

        self.repository.delete(category)

        return {
            "message": "Category deleted successfully"
        }