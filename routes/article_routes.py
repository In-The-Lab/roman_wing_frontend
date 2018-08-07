from flask import Blueprint, request, render_template
from db.dao import PostDAO
from utils import get_current_user

article_blueprint = Blueprint("article", __name__)

@article_blueprint.route("/articles")
def articles_main():
    articles = PostDAO.get_approved_posts()
    return render_template('articles/articles_main.html', articles=articles,
                           current_user=get_current_user())

@article_blueprint.route("/articles/<article_id>")
def articles(article_id):
    article = PostDAO.get_post(int(article_id))
    return render_template('articles/articles.html', article=article,
                           current_user=get_current_user())

@article_blueprint.route("/submit", methods=["GET", "POST"])
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

@article_blueprint.route("/submissions_box")
def check_submissions():
    user = get_current_user()
    if user is None:
        return redirect("/login")
    if not user.is_admin:
        return render_template("index.html",
                               current_user=user,
                               error="You must be an admin to review submissions.")
    submissions = PostDAO.get_unapproved_posts()
    return render_template("submissions_box.html", submissions=submissions)

@article_blueprint.route("/submission/<post_id>")
def review_submission(post_id):
    user = get_current_user()
    if user is None:
        return redirect("/login")
    if not user.is_admin:
        return render_template("index.html",
                               current_user=user,
                               error="You must be an admin to review submissions.")
    post_id = int(post_id)
    submission = PostDAO.get_post(post_id)
    return render_template("submission.html", submission=submission)

@article_blueprint.route("/submissions/<post_id>/review", methods=["GET", "POST"])
def approve_submission(post_id):
    if request.method == "POST":
        user = get_current_user()
        if user is None:
            return redirect("/login")
        if not user.is_admin:
            return render_template("index.html",
                                   current_user=user,
                                   error="You must be an admin to review submissions.")
        post_id = int(post_id)
        updated_text = request.form["body"].replace("\'", "\\'").replace('\"', '\\"')
        print(request.form["result"])
        if request.form["result"] == "approve":
            PostDAO.update_post_text(post_id, updated_text)
            PostDAO.authorize_post(post_id)
            return redirect("/submissions_box")
        else:
            PostDAO.delete_post(post_id)
            return redirect("/submissions_box")
