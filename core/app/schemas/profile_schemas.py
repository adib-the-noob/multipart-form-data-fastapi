from fastapi import UploadFile, File, Form
from pydantic import BaseModel
from datetime import datetime


class ProfileRequest(BaseModel):
    address: str = Form(...)
    role: str = Form(...)
    profile_picture: UploadFile = File(None)


class EducationRequest(BaseModel):
    institution_name: str
    degree: str
    graduated: bool
    starting_date: str
    ending_date: str


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    address: str
    phone_number: str
    profile_picture: str
    created_at: datetime
    updated_at: datetime
