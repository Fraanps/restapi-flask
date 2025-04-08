import pytest
from application import create_app
from config import MockConfig


class TestApplication:
    @pytest.fixture
    def client(self):
        app = create_app(MockConfig, use_mock=True)
        return app.test_client()

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200
