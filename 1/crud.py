from sqlalchemy.orm import Session
from models import Contact, User
from schemas import ContactCreate
from auth import get_password_hash, verify_password
import schemas

def get_contact(db: Session, contact_id: int):
    """
    Retrieve a contact by its ID.

    Args:
        db (Session): Database session.
        contact_id (int): ID of the contact.

    Returns:
        Contact: Contact object or None if not found.
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of contacts with pagination.

    Args:
        db (Session): Database session.
        skip (int): Number of contacts to skip.
        limit (int): Maximum number of contacts to retrieve.

    Returns:
        list: List of contacts.
    """
    return db.query(Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    """
    Create a new contact in the database.

    Args:
        db (Session): Database session.
        contact (ContactCreate): Contact data.

    Returns:
        Contact: Created contact.
    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    """
    Delete a contact by its ID.

    Args:
        db (Session): Database session.
        contact_id (int): ID of the contact to delete.

    Returns:
        Contact: Deleted contact.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(db_contact)
    db.commit()
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    """
    Update an existing contact by its ID.

    Args:
        db (Session): Database session.
        contact_id (int): ID of the contact to update.
        contact (ContactCreate): Updated contact data.

    Returns:
        Contact: Updated contact.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def search_contacts(db: Session, query: str):
    """
    Search for contacts by name or email.

    Args:
        db (Session): Database session.
        query (str): Search query.

    Returns:
        list: List of contacts matching the query.
    """
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f'%{query}%')) |
        (Contact.last_name.ilike(f'%{query}%')) |
        (Contact.email.ilike(f'%{query}%'))
    ).all()

def get_upcoming_birthdays(db: Session):
    """
    Retrieve contacts with birthdays in the next 7 days.

    Args:
        db (Session): Database session.

    Returns:
        list: List of contacts with upcoming birthdays.
    """
    from datetime import datetime, timedelta
    today = datetime.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, next_week)).all()

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email.

    Args:
        db (Session): Database session.
        email (str): Email of the user.

    Returns:
        User: User object or None if not found.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user (UserCreate): User data.

    Returns:
        User: Created user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.

    Args:
        db (Session): Database session.
        email (str): Email of the user.
        password (str): Password of the user.

    Returns:
        User: Authenticated user or False if authentication fails.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
