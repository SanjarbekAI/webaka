from wsgiref.simple_server import make_server


def simple_app(environ, start_response):
    status = "200 OK"
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b"Hello World!"]


server = make_server('localhost', 8000, simple_app)
server.serve_forever()