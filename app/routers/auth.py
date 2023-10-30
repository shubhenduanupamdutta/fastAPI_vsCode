from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..utils import verify_password
from ..database import get_db
from .. import models, oauth2


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    """
    Route to authenticate user

    Args:
        user_credentials (schemas.UserLogin): user data sent with post request
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: when user data is not valid or correct

    Returns:
        json: json with access_token (jwt) and token_type (bearer)
    """
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if (not user) or (not verify_password(user_credentials.password,
                                          user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
