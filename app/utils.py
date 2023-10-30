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
