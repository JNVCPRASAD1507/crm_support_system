
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.customer import Customer
from app.models.user import User


class AuthService:

    @staticmethod
    def register(db: Session, data):
        email = str(data.email).strip().lower()

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            full_name=data.full_name.strip(),
            email=email,
            phone=data.phone,
            password_hash=hash_password(data.password),
            role="customer",
            is_active=True,
        )

        db.add(user)
        db.flush()

        customer = Customer(
            user_id=user.id,
            name=user.full_name,
            email=user.email,
            phone=user.phone,
            status="active",
        )

        db.add(customer)

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ):
        normalized_email = str(email).strip().lower()

        user = (
            db.query(User)
            .filter(User.email == normalized_email)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )

        token = create_access_token(user.id)

        return token, user
