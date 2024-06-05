from webob import Request, Response


class WebAka:
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        user_agent = request.environ.get('HTTP_USER_AGENT', 'USER_AGENT_NOT_FOUND')
        response = Response()
        response.text = f"Hello friend, {user_agent}"
        return response
