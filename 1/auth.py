from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Settings for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for signing JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the provided plain password matches the stored hashed password.

    :param plain_password: The password provided by the user.
    :param hashed_password: The hashed password stored in the database.
    :return: True if the passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a password before storing it in the database.

    :param password: The user's password.
    :return: The hashed version of the password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token.

    :param data: The data to include in the token payload.
    :param expires_delta: The expiration time for the token. Defaults to 15 minutes if not provided.
    :return: The JWT access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """
    Creates a JWT refresh token.

    :param data: The data to include in the token payload.
    :return: The JWT refresh token as a string.
    """
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
