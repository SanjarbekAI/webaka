from app import WebAka

app = WebAka()


@app.route('/home')
def home(request, response):
    response.text = "Hello from the Home Page"


@app.route('/about')
def about(request, response):
    response.text = "Hello from the About Page"


@app.route('/hello/{name}')
def greetings(request, response, name):
    response.text = f"Hello {name}"


@app.route('/books')
class Books:
    def get(self, request, response):
        response.text = "Get method from class"

    def post(self, request, response):
        response.text = "Post method from class"


def new_handler(req, resp):
    resp.text = "From new handler"


@app.route('/template')
def template_handler(req, resp):
    resp.body = app.template(
        'home.html',
        context={
            "new_title": "New title",
            "new_body": "New body"
        }
    )


def on_exception(req, resp, exc):
    resp.text = str(exc)


app.add_exception_handler(on_exception)


@app.route('/exception')
def exception_throwing_handler(req, resp):
    raise AssertionError("some exception")
