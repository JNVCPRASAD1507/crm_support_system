from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.auth import (
    RegisterIn,
    LoginIn,
    Token,
    Profile,
    ProfileUpdate,
    ChangePassword,
)

from app.services.auth_service import AuthService

from app.core.dependencies import (
    get_current_user,
)

from app.core.security import (
    verify_password,
    hash_password,
)


r = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@r.post(
    "/register",
    response_model=Profile,
    status_code=201,
)
def register(
    data: RegisterIn,
    db: Session = Depends(get_db),
):
    user = AuthService.register(
        db,
        data,
    )

    db.commit()
    db.refresh(user)

    return user


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
    user=Depends(get_current_user),
):
    return user


@r.put(
    "/profile",
    response_model=Profile,
)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    for key, value in data.model_dump(
        exclude_none=True
    ).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@r.put("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    if not verify_password(
        data.current_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect",
        )

    user.password_hash = hash_password(
        data.new_password
    )

    db.commit()

    return {
        "message": "Password changed successfully"
    }