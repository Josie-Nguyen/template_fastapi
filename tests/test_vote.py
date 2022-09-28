import pytest
from app import models

@pytest.fixture()
def test_vote(test_post, session, test_user):
    new_vote = models.Vote(post_id = test_post[2].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_post):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 1})
    assert res.status_code ==  201


def test_vote_twice_post(authorized_client, test_post, test_vote):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_post, test_vote):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_none_exist(authorized_client, test_post):
    res = authorized_client.post("/votes/", json={"post_id": test_post[2].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_none_exist(authorized_client, test_post):
    res = authorized_client.post("/votes/", json={"post_id": 110, "dir": 1})
    assert res.status_code ==  404


def test__unauthorized_user(client, test_post):
    res = client.post("/votes/",json={"post_id": test_post[2].id, "dir": 1})
    assert res.status_code == 401