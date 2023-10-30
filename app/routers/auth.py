from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from ..utils import verify_password
from ..database import get_db
from .. import models


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    if (not user) or (not verify_password(user_credentials.password,
                                          user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    return {"token": "example_token"}
