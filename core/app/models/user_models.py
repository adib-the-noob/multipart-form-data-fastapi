import random
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from utils.db_utils.BaseModel import BaseModelMixin
from db import Base  
from config import settings

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    hashed_password = Column(String)

    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="user")
    education = relationship("Education", back_populates="user")
    experience = relationship("Experience", back_populates="user")
    
    def set_username(self):
        self.username = self.full_name.lower().replace(" ", "_") + str(random.randint(100, 999))
