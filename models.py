from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Grant(Base):
    __tablename__ = "grants"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    deadline = Column(DateTime)
    requirements = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    grant_id = Column(Integer, ForeignKey("grants.id"))
    status = Column(String, default="submitted")
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    documents = relationship("Document", back_populates="application")

    # Add the UNIQUE constraint for (user_id, grant_id)
    __table_args__ = (UniqueConstraint("user_id", "grant_id", name="_user_grant_uc"),)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    document_url = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    application = relationship("Application", back_populates="documents")
