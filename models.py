import uuid
from sqlalchemy import String, Integer
from .extensions import db

from sqlalchemy.dialects.postgresql import UUID


# SQLAlchemy 2.0 declarative base
#


class Todo(db.Model):
    # __tablename__ = "todo"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(String(10), nullable=False)
    age = db.Column(Integer, nullable=False)
    email = db.Column(String(255), nullable=False)
    surname = db.Column(String(), nullable=True)
    awd = db.Column(String(), nullable=True)
