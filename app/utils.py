from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Returns hashed password if password is provided

    Args:
        password (str): Password String

    Returns:
        str: Hashed Password
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password):
    """
    Verify that password is correct

    Args:
        password (str): Plain password sent by user
        hashed_password (str): Hashed password from database

    Returns:
        Boolean: True if correct password or False if incorrect
    """
    return pwd_context.verify(password, hashed_password)
