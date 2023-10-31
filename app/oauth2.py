from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    """
    Create jwt token with data provided as a dictionary

    Args:
        data (dict): Data provided to to create access token (jwt)

    Returns:
        jwt: jwt access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema),
                     db: Session = Depends(database.get_db)):
    """
    Verifies that token follows oauth2 schema, returns user from decoding token

    Args:
        token (str, optional): Token provided by frontend. Defaults to
        Depends(oauth2_schema).
        db (Session, optional): Database import. Defaults to Depends
        (database.get_db).

    Returns:
        User: Entry from user database
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_token(token, credential_exception)
    user = db.query(models.User)\
        .filter(models.User.id == token_data.id)\
        .first()
    return user
