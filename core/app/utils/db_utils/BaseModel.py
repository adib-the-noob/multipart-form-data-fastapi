import re
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

class BaseModelMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    