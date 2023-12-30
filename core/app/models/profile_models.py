import datetime
import re
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import Base
from config import settings
from utils.db_utils.BaseModel import BaseModelMixin


class Profile(Base, BaseModelMixin):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")

    role = Column(String, default="student")
    address = Column(String)
    profile_picture = Column(String)

    # make a property to return the profile picture url

    def profile_picture_url(self) -> str | None:
        if self.profile_picture is not None:
            self.profile_picture = self.profile_picture.replace(" ", "%20")
            return f"{settings.BASE_URL}/media/profile_pictures/{self.profile_picture}"
        return None
    
class Education(Base, BaseModelMixin):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="education")

    institution_name = Column(String)
    degree = Column(String)
    graduated = Column(Boolean, default=False)

    starting_date = Column(DateTime)
    ending_date = Column(DateTime)

    def save(self, db):
        # Parse self.ending_date into a datetime object
        ending_date = datetime.datetime.strptime(self.ending_date, "%Y-%m-%d:%H:%M:%S")

        if ending_date > datetime.datetime.now():
            self.graduated = False
        else:
            self.graduated = True

        super().save(db)


class Experience(Base, BaseModelMixin):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="experience")

    company_name = Column(String)
    job_title = Column(String)
    description = Column(String)
    starting_date = Column(DateTime)
    ending_date = Column(DateTime)
