from .. import models, schemas, utils
from ..database import get_db
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Email {user.email} already registered.")

    db.refresh(new_user)

    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {id} not found")
    return user
