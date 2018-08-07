from flask import Blueprint, request, render_template
from db.dao import EventDAO
from utils import get_current_user

event_blueprint = Blueprint("event", __name__)

@event_blueprint.route("/events")
def events_main():
    events = EventDAO.get_all_future_events()
    print(events)
    return render_template('events/events_main.html', events=events,
                           current_user=get_current_user())

@event_blueprint.route("/events/<event_id>")
def events(event_id):
    event = EventDAO.get_event(int(event_id))
    return render_template('events/events.html', event=event,
                           current_user=get_current_user())

@event_blueprint.route("/create_event", methods=["GET", "POST"])
def create_event():
    user = get_current_user()
    if user is None:
        return redirect("/login")
    if not user.is_admin:
        return render_template("index.html",
                               current_user=user,
                               error="You must be an admin to create events.")
    if request.method == "GET":
        return render_template("create_event.html")
    elif request.method == "POST":
        name = request.form["name"]
        desc = request.form["description"]
        date = request.form["date"]
        print(date)
        location = request.form["location"]
        EventDAO.create_event(name, desc, date, location)
        return redirect("/events")
