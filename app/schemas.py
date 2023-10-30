from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    """
    Post model for data validation and easy parsing data from post request for
    social media post

    Args:
        BaseModel (_type_): pydantic base model
    """
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    ...

# class PostUpdate(PostBase):

# Defining a model for response schema
# (for in case if we want to remove some data from db.query)


class Post(PostBase):
    """
    Response Schema, Response must adhere to this format

    Args:
        PostBase (Base Post Model): Above defined PostBase model
    """
    id: int
    # published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Response schema for user"""
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """
    Post request for authentication schema

    Args:
        BaseModel (pydantic.BaseModel): Pydantic Base Model
    """
    email: EmailStr
    password: str
