import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(dict(TESTING=True))

    yield app


@pytest.fixture()
def client(app):
    app.test_client()
