import pytest

from app import WebAka


@pytest.fixture
def app():
    return WebAka()


def test_basic_route_adding(app):
    @app.route('/home')
    def home(req, resp):
        resp.text = "Hello from Home Page"


def test_duplicate_routes_throw_exception(app):
    @app.route('/home')
    def home(req, resp):
        resp.text = "Hello from Home Page"

    with pytest.raises(AssertionError):
        @app.route('/home')
        def home2(req, resp):
            resp.text = "Hello from Home Page"
