from flask import Flask, request, render_template
from db.dao import UserDAO, PostDAO, EventDAO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/log-in")
def login():
    return render_template('login.html')

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

@app.route("/profile/<profile_id>")
def profile(profile_id):
    user = UserDAO.get_user(int(profile_id))
    return render_template('profiles.html', profile=user)

@app.route("/submit")
def submit():
    return render_template('submit.html')

if __name__ == "__main__":
    app.run(debug=True)
