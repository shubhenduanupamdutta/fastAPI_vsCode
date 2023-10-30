"""
Fast API app for tutorial on freeCodeCamp
by Sanjeev Thyagarajan

"""

# import time
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
# from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session
# from config import config  # load data from .env
from . import models, schemas, utils


# load database tables i.e. models
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host=config.HOST,
#                                 dbname=config.DB_NAME,
#                                 user=config.USER,
#                                 password=config.PASSWORD,
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection to database was successful.")
#         break
#     except Exception as e:
#         print("Connection to database failed")
#         print(f"Error: {e}")
#         time.sleep(5)


@app.get("/")
def root():
    """
    Root directory get method

    Returns:
        json: "message"
    """
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    """
    Generate all the posts stored

    Returns:
        json: jsonified all post data
    """
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED,
          response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
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
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the post with id = post_id and return the posts

    Args:
        post_id (int): An integer which is the id of the post to be retrieved

    Returns:
        dict: retrieved post in dictionary format
    """
    # cursor.execute("""SELECT * FROM posts WHERE id = %(int)s""",
    #                {'int': post_id})
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )

    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete post with id of id.

    Args:
        id (int): id of the post to be deleted

    Raises:
        HTTPException: Raises 404 if the post is not found

    Returns:
        dict: message details
    """
    # cursor.execute("""DELETE FROM posts
    #                WHERE id = %(int)s
    #                RETURNING * """,
    #                {'int': post_id})
    # deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    post_query.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate,
                db: Session = Depends(get_db)):
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
    # cursor.execute("""UPDATE posts SET
    #                title = %(title)s,
    #                content = %(cont)s ,
    #                published = %(bool)s
    #                WHERE id = %(int)s RETURNING *""",
    #                {'title': post.title, 'cont': post.content,
    #                 'bool': post.published, 'int': post_id})
    # new_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    post_query.update(post.model_dump(),  # type: ignore
                      synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED,
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
