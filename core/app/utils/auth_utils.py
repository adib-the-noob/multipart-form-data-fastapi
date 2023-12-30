from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


from config import settings
from db import db_dependency
from models.user_models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(email: str, db: db_dependency):
    user = db.query(User).filter(User.email == email, User.is_verified==True).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not verified or not found!",
        )
    return user


def authenticate_user(email: str | None, password: str, db: db_dependency) -> dict:
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.AlGORITHM
    )
    return encoded_jwt


def create_user(
    email: str, password: str, phone_number: str, full_name: str, db: db_dependency
):
    if email is not None:
        user = db.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user = User(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            phone_number=phone_number,
        )
        user.set_username()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


def get_current_user(token: Annotated[str, Depends(oauth_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.AlGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
