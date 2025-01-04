import inspect
import os.path

import requests
import wsgiadapter
from parse import parse
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader


class WebAka:
    def __init__(self, templates_dir="templates"):
        self.routes = dict()
        self.template_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, "Duplicate route error. Please change the URL."
        self.routes[path] = handler

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    response.status_code = 405
                    response.text = "Method Not Allowed"
                    return response

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request):
        for path, handler in self.routes.items():
            parsed_result = parse(path, request.path)
            if parsed_result is not None:
                return handler, parsed_result.named
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found"

    def test_session(self):
        session = requests.Session()
        session.mount("http://testserver", wsgiadapter.WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = dict()

        return self.template_env.get_template(template_name).render(**context).encode()
