import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = [schemas.PostOut(**post) for post in res.json()]
    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888888")
    assert res.status_code == 404


@pytest.mark.parametrize("index", [0, 1, 2])
def test_get_one_post(authorized_client, test_posts, index):
    res = authorized_client.get(f"/posts/{test_posts[index].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[index].id
    assert post.Post.title == test_posts[index].title
    assert post.Post.content == test_posts[index].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "some new content", True),
    ("Fav Pizza", "Cheese Burst", True),
    ("My love", "My wife bubu", False),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title, "content": content, "published": published
    })
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={
        "title": "something", "content": "some interesting content"
    })
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "something"
    assert created_post.content == "some interesting content"
    assert created_post.published
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user):
    res = client.post("/posts/", json={
        "title": "something", "content": "some interesting content"
    })
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


@pytest.mark.parametrize("index", [0, 1, 2])
def test_delete_post(authorized_client, test_user, test_posts, index):
    res = authorized_client.delete(f"/posts/{test_posts[index].id}")
    assert res.status_code == 204


def test_delete_post_non_existent(authorized_client, test_posts):
    res = authorized_client.delete("/posts/45132431")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


@pytest.mark.parametrize("index", [0, 1, 2])
def test_update_post(authorized_client, test_user, test_posts, index):
    data = {
        "title": "updated title",
        "content": "updated conent",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[index].id}", json=data)

    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.id == test_posts[index].id


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated conent",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated conent",
        "published": False
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_non_existent(authorized_client):
    data = {
        "title": "updated title",
        "content": "updated conent",
        "published": False
    }
    res = authorized_client.put("/posts/45132431", json=data)
    assert res.status_code == 404
