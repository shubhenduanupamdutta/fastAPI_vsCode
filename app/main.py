"""
Fast API app for tutorial on freeCodeCamp
by Sanjeev Thyagarajan

"""
from random import randrange
from typing import Any
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel


app = FastAPI()


POSTS: list[dict[str, Any]] = [
    {"title": "my name", "content": "Shubhendu", "id": 1},
    {"title": "Beaches on florida", "content": "Beaches", "id": 2}
]


def find_post(post_id: int) -> dict[str, Any] | None:
    """
    Finds specific post with id = post_id from all posts

    Args:
        post_id (int): id of the post to be retrieved

    Returns:
        dict[str, Any] | None: returns the post as a dictionary
    """
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


class Post(BaseModel):
    """
    Post model for data validation and easy parsing data from post request for social media post

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


@app.get("/posts")
def get_posts():
    """
    Generate all the posts stored

    Returns:
        json: jsonified all post data
    """
    return {"data": POSTS}


@app.post("/create-post")
def create_post_body(payload: dict = Body(...)):
    """
    Takes in a post request to create a post and does the operation to store data.

    Returns:
        json: returns a message describing the result (success or failure)
    """
    # print(payload)
    response_msg = {"response": "Success, new post created."}
    response_msg["new_post"] = f"title {payload['title']} content {payload['content']}"
    return response_msg


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    """
    Takes in data from post request validates using pydantic and operates on it as needed.

    Args:
        new_post (Post): Data from post request, in the format of Post class defined

    Returns:
        json: success or failure message
    """
    new_post_dict = new_post.model_dump()
    new_post_dict["id"] = randrange(0, 10000000000)
    response_msg: dict[str, Any] = {"response": "Success, new post created"}
    response_msg["new_post"] = new_post_dict
    POSTS.append(new_post_dict)
    return response_msg


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Retrieve the post with id = post_id and return the posts

    Args:
        post_id (int): An integer which is the id of the post to be retrieved

    Returns:
        dict: retrieved post in dictionary format
    """
    post = find_post(post_id)
    if not post:
        # One way to get required status_code
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id = {post_id} not found."}

        # Better Way
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    # print(post)
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
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    POSTS.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    """
    Updates old post if new data and old post id is provided.

    Args:
        post_id (int): id of the post to be updated
        updated_post (Post): New content of the post (all required content needs to be provided)

    Raises: 
        HTTPException: raises 404 if post is not found in database

    Returns:
        json: message containing new post details
        
    """
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {post_id} was not found"
                            )
    post_dict = updated_post.model_dump()
    post_dict["id"] = post_id
    POSTS[POSTS.index(post)] = post_dict
    return {"data": post_dict}
