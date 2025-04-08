import pytest
from application import create_app
from config import MockConfig


class TestApplication:
    @pytest.fixture
    def client(self):
        app = create_app(MockConfig, use_mock=True)
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "name": "Francilene",
            "last_name": "Silva",
            "cpf": "286.324.800-65",
            "email": "fran@gmail.com",
            "birth_date": "1994-04-08"
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "name": "Francilene",
            "last_name": "Silva",
            "cpf": "018.396.920-16",
            "email": "fran@gmail.com",
            "birth_date": "1994-04-08"
        }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"successfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"CPF is invalid" in response.data
