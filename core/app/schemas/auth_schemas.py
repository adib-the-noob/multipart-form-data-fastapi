from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRequest(BaseModel):
    email: str
    password: str
    full_name: str
    phone_number: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool

class OtpVerificationRequest(BaseModel):
    otp: int
    email: str