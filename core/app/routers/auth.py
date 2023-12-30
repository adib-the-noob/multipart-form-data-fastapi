from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, ORJSONResponse
from jose import jwt, JWTError
from config import settings

import random

from utils.auth_utils import (
    authenticate_user,
    create_user,
    create_access_token,
    get_current_user,
)
from utils.caching_utils import (
    otp_cache,
)

from db import db_dependency

from schemas.auth_schemas import Token, UserRequest, UserResponse
from schemas import profile_schemas, auth_schemas
from models.user_models import User
from models.profile_models import Profile

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

current_user = Annotated[User, Depends(get_current_user)]


@router.post("/create-user", response_model=None, status_code=status.HTTP_201_CREATED)
async def register(user: UserRequest, db: db_dependency):
    user = create_user(
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        full_name=user.full_name,
        db=db,
    )
    if user is not None:
        otp_cache.generate_otp(user.id, otp=random.randint(1000, 9999))
        return ORJSONResponse(
            {"message": "User created successfully! Please verify with OTP."}
        )
    return ORJSONResponse(
        {"message": "Something went wrong!"}, status_code=status.HTTP_400_BAD_REQUEST
    )


@router.post("/verify-otp", response_model=None, status_code=status.HTTP_200_OK)
def verify_otp(otp_verifier: auth_schemas.OtpVerificationRequest, db: db_dependency):
    user = db.query(User).filter(User.email == otp_verifier.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found!"
        )
    otp = otp_cache.get_otp(user.id)
    if otp is None or otp != otp_verifier.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found!"
        )
    token = create_access_token(data={"sub": user.email, "id": user.id})
    user.is_verified = True
    user.save(db)
    return ORJSONResponse(
        {
            "message": "OTP verified successfully!",
            "data": {
                "access_token": token,
                "token_type": "bearer",
            },
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/token", response_model=None)
async def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    if form_data.username is None and form_data.email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user = authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(data={"sub": user.email, "id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)], db: db_dependency
):
    return JSONResponse(
        {
            "data": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "phone_number": current_user.phone_number,
            }
        }
    )
