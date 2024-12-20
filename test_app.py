import uuid

import pytest


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


def test_request_can_be_sent_by_test_client(app, test_client):
    @app.route('/home')
    def home(req, resp):
        resp.text = "Hello from Home Page"

    response = test_client.get("http://testserver/home")

    assert response.text == "Hello from Home Page"


def test_parameterized_routing(app, test_client):
    @app.route('/hello/{name}')
    def greetings(request, response, name):
        response.text = f"Hello {name}"

    assert test_client.get("http://testserver/hello/Sanjarbek").text == "Hello Sanjarbek"
    assert test_client.get("http://testserver/hello/2002").text == "Hello 2002"


def test_default_response(test_client):
    response = test_client.get(f"http://testserver/{uuid.uuid4()}")
    assert response.text == "Not Found"
    assert response.status_code == 404


def test_class_based_get(app, test_client):
    @app.route('/books')
    class Books:
        def get(self, request, response):
            response.text = "Get method from class"

    assert test_client.get("http://testserver/books").text == "Get method from class"


def test_class_based_post(app, test_client):
    @app.route('/books')
    class Books:
        def post(self, request, response):
            response.text = "Post method from class"

    assert test_client.post("http://testserver/books").text == "Post method from class"


def test_class_not_allowed_method(app, test_client):
    @app.route('/books')
    class Books:
        def post(self, request, response):
            response.text = "Post method from class"

    response = test_client.get("http://testserver/books")

    assert response.text == "Method Not Allowed"
    assert response.status_code == 405


def test_alternative_route_adding(app, test_client):
    def new_handler(req, resp):
        resp.text = "From new handler"

    app.add_route('/new-handler', new_handler)
    assert test_client.get("http://testserver/new-handler").text == "From new handler"
