from flask import Flask, requests, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(index.html)

@app.route("/articles_main")
def articles_main():
    return render_template(articles_main.html)

@app.route("/articles/<int:article_id>")
def articles():
    return render_template(articles.html)

@app.route("/events_main")
def events_main():
    return render_template(events_main.html)

@app.route("/events/<int:event_id>")
def events():
    return render_template(events.html)

@app.route("/profile/<profile_name>")
def profile():
    return render_template(profiles.html)

@app.route("/submit")
def submit():
    return render_template(submit.html)

if __name__ == "__main__":
    app.run(debug=True)
