from pydantic import BaseModel


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


class Post(BaseModel):
    """
    Response Schema, Response must adhere to this format

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    title: str
    content: str
    published: bool
