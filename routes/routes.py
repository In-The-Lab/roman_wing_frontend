from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from db.dao import UserDAO, PostDAO, EventDAO, AuthDAO
import configparser
import bcrypt

app = Flask(__name__, template_folder="../templates", static_folder="../static")
config = configparser.ConfigParser()
config.read("../config/config.ini")
app.secret_key = config["APP"]["secret"].encode("utf-8")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserDAO.get_user(user_id)

@app.route("/")
def index():
    try:
        curr_usr_id = current_user.id
        return render_template('index.html', current_user=current_user)
    except:
        return render_template('index.html', current_user=None)

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
    articles = PostDAO.get_all_posts()
    return render_template('articles/articles_main.html', articles=articles)

@app.route("/articles/<article_id>")
def articles(article_id):
    article = PostDAO.get_post(int(article_id))
    return render_template('articles/articles.html', article=article)

@app.route("/events")
def events_main():
    events = EventDAO.get_all_future_events()
    return render_template('events/events_main.html', events=events)

@app.route("/events/<event_id>")
def events(event_id):
    event = EventDAO.get_event(int(event_id))
    return render_template('events/events.html', event=event)

@login_required
@app.route("/profile/<profile_id>")
def profile(profile_id):
    user = current_user
    if current_user.id != int(profile_id):
        return render_template('index.html',
                               error="You can only view your own profile")
    return render_template('profiles.html', profile=user)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/submit")
def submit():
    return render_template('submit.html')

app.run(debug=True)
