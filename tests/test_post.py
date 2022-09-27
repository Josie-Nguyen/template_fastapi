import json
from urllib import response
import pytest
from typing import List
from app import schemas

def test_get_all_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, res.json())
    post_list = list(post_map)
    assert len(res.json()) == len(test_post)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get(f"/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/12")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_post[0].id
    assert post.Post.content == test_post[0].content
    assert post.Post.title == test_post[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("test title", "test content", True),
    ("this is my", "this is my", False)
])

def test_create_post(authorized_client, test_user, test_post, title, content, published):
    res = authorized_client.post(
        "/posts/",json={"title": title, "content": content, "published": published})

    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_post):
    res = authorized_client.post(
        "/posts/",json={"title": "test title", "content": "test content"})

    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == "test title"
    assert create_post.content == "test content"
    assert create_post.published == True
    assert create_post.owner_id == test_user['id']


def test_unauthorized_user_create_posts(client, test_post, test_user):
    res = client.get("/posts/", json={"title": "test title", "content": "test content"})
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_post, test_user):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204

def test_delete_post_none_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/117")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[2].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_post):
    data ={
        "title": "test update",
        "content": "updated content",
        "id": test_post[0].id
    }

    res = authorized_client.put(f"/posts/{test_post[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_updat_other_user_post(authorized_client, test_user1, test_user, test_post):
    data = {
        "title" : "updated title",
        "content": "updated content",
        "id": test_post[2].id
    }
    res = authorized_client.put(f"/posts/{test_post[2].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_update_post(client, test_post, test_user):
    res = client.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_update_post_none_exist(authorized_client, test_user, test_post):
    data = {
        "title" : "updated title",
        "content": "updated content",
        "id": test_post[2].id
    }
    res = authorized_client.put("/posts/117", json=data)
    assert res.status_code == 404