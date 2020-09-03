from flask import Flask, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index_page():
    return 'Index page'


@app.route("/welcome/<username>")
def hello_user(username):
    return f"Welcome, {escape(username)}!"


@app.route('/login')
def login():
    return 'login'


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    return f"post id is {post_id}"


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route("/test", methods=["POST", "GET"])
def login_user():
    print("inside")
    error = None
    if request.method == "POST":
        # print(request["email"])
        # print(request["password"])
        return "OK"
    else:
        error = 'Invalid username/password'
    return error


with app.test_request_context():
    print(url_for('index_page'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('hello_user', username='John Doe'))
    print(url_for('static', filename='style.css'))
