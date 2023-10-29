"""
Fast API app for tutorial on freeCodeCamp
by Sanjeev Thyagarajan

"""

import time
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from config import config  # load data from .env
from . import models

# load database tables i.e. models
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host=config.HOST,
                                dbname=config.DB_NAME,
                                user=config.USER,
                                password=config.PASSWORD,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to database was successful.")
        break
    except Exception as e:
        print("Connection to database failed")
        print(f"Error: {e}")
        time.sleep(5)


class Post(BaseModel):
    """
    Post model for data validation and easy parsing data from post request for
    social media post

    Args:
        BaseModel (_type_): pydantic base model
    """
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    """
    Root directory get method

    Returns:
        json: "message"
    """
    return {"message": "Welcome to my API"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """
    Generate all the posts stored

    Returns:
        json: jsonified all post data
    """
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    """
    Takes in data from post request validates using pydantic and operates on
    it as needed.

    Args:
        new_post (Post): Data from post request, in the format of Post class
        defined

    Returns:
        json: success or failure message
    """
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s)
    #                RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "Successfully added post", "data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Retrieve the post with id = post_id and return the posts

    Args:
        post_id (int): An integer which is the id of the post to be retrieved

    Returns:
        dict: retrieved post in dictionary format
    """
    cursor.execute("""SELECT * FROM posts WHERE id = %(int)s""",
                   {'int': post_id})
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )

    return {"message": f"Here is your post with id = {post_id}",
            "post": post
            }


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """
    Delete post with id of id.

    Args:
        id (int): id of the post to be deleted

    Raises:
        HTTPException: Raises 404 if the post is not found

    Returns:
        dict: message details
    """
    cursor.execute("""DELETE FROM posts
                   WHERE id = %(int)s
                   RETURNING * """,
                   {'int': post_id})
    deleted_post = cursor.fetchone()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    """
    Updates old post if new data and old post id is provided.

    Args:
        post_id (int): id of the post to be updated
        updated_post (Post): New content of the post (all required content
        needs to be provided)

    Raises:
        HTTPException: raises 404 if post is not found in database

    Returns:
        json: message containing new post details

    """
    cursor.execute("""UPDATE posts SET
                   title = %(title)s,
                   content = %(cont)s ,
                   published = %(bool)s
                   WHERE id = %(int)s RETURNING *""",
                   {'title': post.title, 'cont': post.content,
                    'bool': post.published, 'int': post_id})
    new_post = cursor.fetchone()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    conn.commit()
    return {"data": new_post}
