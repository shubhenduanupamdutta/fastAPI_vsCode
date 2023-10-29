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
