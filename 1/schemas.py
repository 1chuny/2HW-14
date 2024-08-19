from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ContactBase(BaseModel):
    """
    Base schema for contact information.

    Attributes:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (EmailStr): The email address of the contact.
        phone (str): The phone number of the contact.
        birthday (date): The birthday of the contact.
        additional_info (Optional[str]): Any additional information about the contact.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    """
    Schema for creating a new contact.

    Inherits from:
        ContactBase: Inherits all attributes from ContactBase.
    """
    pass

class Contact(ContactBase):
    """
    Schema representing a contact, including ID and owner ID.

    Attributes:
        id (int): The unique identifier of the contact.
        owner_id (int): The ID of the user who owns the contact.

    Config:
        orm_mode (bool): Enables ORM mode to interact with SQLAlchemy models.
    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    """
    Base schema for user information.

    Attributes:
        email (EmailStr): The email address of the user.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        password (str): The password for the user account.

    Inherits from:
        UserBase: Inherits the email attribute from UserBase.
    """
    password: str

class User(UserBase):
    """
    Schema representing a user, including ID, verification status, and avatar.

    Attributes:
        id (int): The unique identifier of the user.
        is_verified (bool): Indicates whether the user's email is verified.
        avatar (Optional[str]): The URL of the user's avatar image.

    Config:
        orm_mode (bool): Enables ORM mode to interact with SQLAlchemy models.
    """
    id: int
    is_verified: bool
    avatar: Optional[str] = None

    class Config:
        orm_mode = True
