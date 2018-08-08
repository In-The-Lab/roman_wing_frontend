from flask import Blueprint, request, redirect, render_template
from flask_login import login_user, current_user, logout_user
from db.dao import UserDAO, AuthDAO
from utils import get_current_user, collect_from_db_for_index
import bcrypt

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/signup", methods=["GET", "POST"])
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

@user_blueprint.route("/login", methods=["GET", "POST"])
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

@user_blueprint.route("/profile/<profile_id>")
def profile(profile_id):
    user = get_current_user()
    print(user)
    if current_user.id != int(profile_id):
        articles, events = collect_from_db_for_index()
        return render_template('index.html',
                               error="You can only view your own profile",
                               current_user=get_current_user(),
                               articles=articles,
                               events=events)
    return render_template('profiles.html', profile=user,
                           current_user=user)

@user_blueprint.route("/logout")
def logout():
    current_user = get_current_user()
    if current_user is None:
        articles, events = collect_from_db_for_index()
        return render_template("index.html", current_user=None,
                               articles=articles, events=events)
    logout_user()
    return redirect("/")
