from app import WebAka

app = WebAka()


@app.route('/home')
def home(request, response):
    response.text = "Hello from the Home Page"


@app.route('/about')
def about(request, response):
    response.text = "Hello from the About Page"
