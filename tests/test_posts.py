from fastapi.testclient import TestClient
from mb import get_app
from unittest.mock import patch
import pytest
from datetime import datetime, timezone


@pytest.fixture
def token_payload():
    with patch("mb.auth.get_payload") as mock_get_user_id:
        mock_get_user_id.return_value = {"sub": "usr_123"}
        yield mock_get_user_id
        return


@pytest.fixture(autouse=True)
def instant_storage():
    with patch("mb.storage.sleep") as sleep:
        yield sleep


@pytest.fixture
def client():
    app = get_app()
    return TestClient(app)


class TestPostCreate:
    def test_create(self, token_payload, client):
        response = client.post(
            "/posts",
            json={"title": "Test post", "content": "Long time no see."},
            headers={"Authorization": "Bearer test"},
        )
        posts = list(client.app.storage.posts.values())
        assert response.status_code == 200
        assert posts[0].title == "Test post"
        assert posts[0].content == "Long time no see."
        assert posts[0].author == "usr_123"

    def test_fails_with_no_auth(self, client):
        response = client.post(
            "/posts",
            json={"title": "Test", "content": "Test"},
        )
        assert response.status_code == 403


class TestPostList:
    def test_list(self, client):
        client.app.storage.posts["post_ABCDEF"] = {
            "id": "post_ABCDEF",
            "title": "Test post (for listing)",
            "content": "Long time no see",
            "author": "usr_123",
            "created_at": datetime(2024, 4, 25, 12, 0, 1, 12, tzinfo=timezone.utc),
        }
        response = client.get("/posts")
        assert response.status_code == 200
        assert response.json() == {
            "posts": [
                {
                    "id": "post_ABCDEF",
                    "title": "Test post (for listing)",
                    "content": "Long time no see",
                    "author": "usr_123",
                    "created_at": "2024-04-25T12:00:01.000012Z",
                }
            ]
        }
