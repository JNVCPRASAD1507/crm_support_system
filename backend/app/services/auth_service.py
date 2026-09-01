from fastapi import HTTPException, status

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.repositories.user_repository import UserRepository
from app.repositories.customer_repository import CustomerRepository


class AuthService:

    @staticmethod
    def register(db, data):

        user_repo = UserRepository(db)
        customer_repo = CustomerRepository(db)

        # Check duplicate email
        existing_user = user_repo.by_email(
            data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Convert enum to string
        role = data.role.value

        # Create User
        user = user_repo.create(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(
                data.password
            ),
            role=role,
            is_active=True,
        )

        # Only customers get a Customer profile.
        if role == "customer":
            customer_repo.create(
                user_id=user.id,
                name=data.full_name,
                email=data.email,
                phone=data.phone,
                status="active",
            )

        return user

    @staticmethod
    def login(db, email, password):

        user_repo = UserRepository(db)

        user = user_repo.by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account inactive",
            )

        token = create_access_token(
            user.id
        )

        return token, user