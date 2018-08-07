from flask import Flask, render_template, session
from flask_login import LoginManager, logout_user, current_user
from flask_login import login_user, login_required
from flask_socketio import SocketIO, emit
from db.dao import UserDAO, PostDAO, EventDAO
from db.models import Post
from user_routes import user_blueprint
from event_routes import event_blueprint
from article_routes import article_blueprint
from utils import get_current_user, user
import configparser

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.register_blueprint(user_blueprint)
app.register_blueprint(event_blueprint)
app.register_blueprint(article_blueprint)

config = configparser.ConfigParser()
config.read("../config/config.ini")
app.secret_key = config["APP"]["secret"].encode("utf-8")

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return UserDAO.get_user(user_id)
Post.user = user

socketio = SocketIO(app)
@socketio.on('disconnect')
def disconnect_user():
    logout_user()

@app.route("/")
def index():
    articles = PostDAO.get_approved_posts()
    articles.sort(key=lambda p: p.date_created, reverse=True)
    most_recent_events = EventDAO.get_all_future_events()
    if len(articles) > 10:
        articles = articles[:10]
    return render_template("index.html", current_user=get_current_user(),
                           articles=articles, events=most_recent_events)

app.run(debug=True)
