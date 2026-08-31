
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    ChangePassword,
    LoginIn,
    Profile,
    ProfileUpdate,
    RegisterIn,
    Token,
)
from app.services.auth_service import AuthService


r = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@r.post(
    "/register",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterIn,
    db: Session = Depends(get_db),
):
    try:
        user = AuthService.register(db, data)

        db.commit()
        db.refresh(user)

        return user

    except Exception:
        db.rollback()
        raise


@r.post(
    "/login",
    response_model=Token,
)
def login(
    data: LoginIn,
    db: Session = Depends(get_db),
):
    token, _ = AuthService.login(
        db,
        data.email,
        data.password,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@r.get(
    "/profile",
    response_model=Profile,
)
def profile(
    user: User = Depends(get_current_user),
):
    return user


@r.put(
    "/profile",
    response_model=Profile,
)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    values = data.model_dump(
        exclude_none=True,
    )

    if "full_name" in values:
        values["full_name"] = values["full_name"].strip()

    for key, value in values.items():
        setattr(user, key, value)

    # Keep customer profile synchronized with account data.
    if user.customer:
        if "full_name" in values:
            user.customer.name = values["full_name"]

        if "phone" in values:
            user.customer.phone = values["phone"]

    db.commit()
    db.refresh(user)

    return user


@r.put("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not verify_password(
        data.current_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    if verify_password(
        data.new_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    user.password_hash = hash_password(
        data.new_password,
    )

    db.commit()

    return {
        "message": "Password changed successfully",
    }
