from typing import Annotated, Optional
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse, ORJSONResponse


from config import settings
from utils.auth_utils import (
    get_current_user,
)


from db import db_dependency
from models import profile_models, user_models
from schemas import profile_schemas
from models.user_models import User
from models.profile_models import Profile

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)

current_user = Annotated[User, Depends(get_current_user)]


@router.post("/create-profile", response_model=profile_schemas.ProfileResponse)
def create_profile(
    user: current_user,
    db: db_dependency,
    profile: profile_schemas.ProfileRequest = Depends(),
):
    if db.query(Profile).filter(Profile.user_id == user.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists",
        )

    if profile.profile_picture is not None:
        if not os.path.exists("media/profile_pictures"):
            os.makedirs("media/profile_pictures")
        # create a media folder in the root directory
        with open(
            f"media/profile_pictures/{profile.profile_picture.filename}", "wb"
        ) as buffer:
            buffer.write(profile.profile_picture.file.read())

    profile = Profile(
        user_id=user.id,
        address=profile.address,
        role=profile.role,
        profile_picture=profile.profile_picture.filename
        if profile.profile_picture
        else None,
    )
    profile.save(db)

    return ORJSONResponse(
        {
            "data": {
                "id": profile.id,
                "user_id": profile.user_id,
                "address": profile.address,
                "profile_picture": profile.profile_picture_url(),
            }
        }
    )


@router.get("/get-profile", response_model=profile_schemas.ProfileResponse)
def get_profile(user: current_user, db: db_dependency):
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return JSONResponse(
        {
            "data": {
                "address": profile.address,
                "role": profile.role,
                "profile_picture": profile.profile_picture_url(),
            }
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/create-edu", response_model=None)
def create_education(
    user: current_user,
    db: db_dependency,
):
    profile_models.Education(
        user_id=user.id,
        institution_name="Universitas Indonesia",
        degree="Sarjana",
        starting_date="2017-09-01:00:00:00",
        ending_date="2021-09-01:00:00:00",
    ).save(db)
    return JSONResponse(
        {
            "data": {
                "message": "Education created successfully",
            }
        },
        status_code=status.HTTP_200_OK,
    )
