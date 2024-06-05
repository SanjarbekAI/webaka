from webob import Request, Response


class WebAka:
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()
        response.text = "Hello world"
        return response(environ, start_response)
