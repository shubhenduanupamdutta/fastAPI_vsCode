from datetime import datetime, timedelta
from jose import jwt
from .config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(data: dict):
    """
    Create jwt token with data provided as a dictionary

    Args:
        data (dict): Data provided to to create access token (jwt)

    Returns:
        jwt: jwt access token
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
