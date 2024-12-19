import pytest

from app import WebAka


@pytest.fixture
def app():
    return WebAka()


@pytest.fixture
def test_client(app):
    return app.test_session()
