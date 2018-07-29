from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/articles")
def articles_main():
    return render_template('articles/articles_main.html')

@app.route("/articles/<article_name>")
def articles(article_name):
    return render_template('articles/articles.html', article=article_name)

@app.route("/events")
def events_main():
    return render_template('events/events_main.html')

@app.route("/events/<event_name>")
def events(event_name):
    return render_template('events/events.html', event=event_name)

@app.route("/profile/<profile_name>")
def profile(profile_name):
    return render_template('profiles.html', profile=profile_name)

@app.route("/submit")
def submit():
    return render_template('submit.html')

if __name__ == "__main__":
    app.run(debug=True)
