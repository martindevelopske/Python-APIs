import pytest
from app import models


@pytest.fixture()
def test_like(test_posts, session, test_user):
    new_like = models.Like(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201


def test_like_twice_post(authorized_client, test_posts, test_like):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_like(authorized_client, test_posts, test_like):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_like_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_like_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404


def test_like_unauthorized_user(client, test_posts):
    res = client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401