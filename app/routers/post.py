from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              current_user=Depends(oauth2.get_current_user)):
    """
    Generate all the posts stored

    Returns:
        json: jsonified all post data
    """
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
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

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db),
             current_user=Depends(oauth2.get_current_user)):
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


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
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
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action.")
    post_query.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
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
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform this action.")
    post_query.update(updated_post.model_dump(),  # type: ignore
                      synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()
