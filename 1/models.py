"""
Database models module.

This module defines the SQLAlchemy models for users and contacts.
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """
        User model.

        Represents a user in the database.
        """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    """
       Contact model.

       Represents a contact in the database.
       """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="contacts")
