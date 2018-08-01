from flask import Flask, request, render_template, redirect, session
from flask_login import LoginManager, logout_user, current_user
from flask_login import login_user, login_required
from flask_socketio import SocketIO, emit
from db.dao import UserDAO, PostDAO, EventDAO, AuthDAO
import configparser
import bcrypt

app = Flask(__name__, template_folder="../templates", static_folder="../static")
config = configparser.ConfigParser()
config.read("../config/config.ini")
app.secret_key = config["APP"]["secret"].encode("utf-8")

login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return UserDAO.get_user(user_id)

def get_current_user():
    try:
        id = current_user.id
        return current_user
    except:
        return None

@app.route("/")
def index():
    return render_template("index.html", current_user=get_current_user())

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        p1 = request.form["password"]
        p2 = request.form["confirm_password"]
        if p1 != p2:
            err = "Passwords don't match."
            return render_template("signup.html", err=err)
        hash = bcrypt.hashpw(p1.encode("utf-8"), bcrypt.gensalt())
        UserDAO.insert_user(first_name, last_name, email)
        usr = UserDAO.get_user_by_email(email)
        AuthDAO.insert_hash(usr.id, hash)
        login_user(usr)
        return redirect("/profile/{}".format(usr.id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form["email"]
        usr = UserDAO.get_user_by_email(email)
        if usr is None:
            return render_template('login.html', error="No such user exists")
        password = request.form["password"]
        if bcrypt.checkpw(password.encode("utf-8"), AuthDAO.get_hash(usr.id)):
            login_user(usr)
            return redirect("/profile/{}".format(usr.id))
        else:
            return render_template('login.html', error="Incorrect password")

@app.route("/articles")
def articles_main():
    articles = PostDAO.get_approved_posts()
    return render_template('articles/articles_main.html', articles=articles,
                           current_user=get_current_user())

@app.route("/articles/<article_id>")
def articles(article_id):
    article = PostDAO.get_post(int(article_id))
    return render_template('articles/articles.html', article=article,
                           current_user=get_current_user())

@app.route("/events")
def events_main():
    events = EventDAO.get_all_future_events()
    return render_template('events/events_main.html', events=events,
                           current_user=get_current_user())

@app.route("/events/<event_id>")
def events(event_id):
    event = EventDAO.get_event(int(event_id))
    return render_template('events/events.html', event=event,
                           current_user=get_current_user())

@app.route("/profile/<profile_id>")
def profile(profile_id):
    user = get_current_user()
    if current_user.id != int(profile_id):
        return render_template('index.html',
                               error="You can only view your own profile",
                               current_user=get_current_user())
    return render_template('profiles.html', profile=user,
                           current_user=get_current_user())

@app.route("/logout")
def logout():
    current_user = get_current_user()
    if current_user is None:
        return render_template("index.html", current_user=None)
    logout_user()
    return redirect("/")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return render_template('submit.html', current_user=get_current_user())
    elif request.method == "POST":
        user = get_current_user()
        if current_user is None:
            return render_template("index.html", current_user=None)
        title = request.form["title"]
        description = request.form["description"]
        thumbnail_url = request.form["thumbnail_url"]
        body = request.form["body"]
        PostDAO.insert_post(user.id, title, description, body, thumbnail_url)
        return redirect("/articles")

@app.route("/submissions_box")
def check_submissions():
    user = get_current_user()
    if user is None:
        return redirect("/login")
    if not user.is_admin:
        return render_template("/", error="You must be an admin to review submissions.")
    submissions = PostDAO.get_unapproved_posts()
    return render_template("submissions_box.html", submissions=submissions)

@app.route("/submission/<post_id>")
def review_submission(post_id):
    user = get_current_user()
    if user is None:
        return redirect("/login")
    if not user.is_admin:
        return render_template("/", error="You must be an admin to review submissions.")
    post_id = int(post_id)
    submission = PostDAO.get_post(post_id)
    return render_template("submission.html", submission=submission)

@app.route("/submissions/<post_id>/review", methods=["GET", "POST"])
def approve_submission(post_id):
    if request.method == "POST":
        user = get_current_user()
        if user is None:
            return redirect("/login")
        if not user.is_admin:
            return render_template("/", error="You must be an admin to review submissions.")
        post_id = int(post_id)
        updated_text = request.form["body"]
        print(request.form["result"])
        if request.form["result"] == "approve":
            PostDAO.update_post_text(post_id, updated_text)
            PostDAO.authorize_post(post_id)
            return redirect("/submissions_box")
        else:
            PostDAO.delete_post(post_id)
            return redirect("/submissions_box")

@socketio.on('disconnect')
def disconnect_user():
    logout_user()

app.run(debug=True)
