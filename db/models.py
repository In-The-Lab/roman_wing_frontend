import json

class User:

    def __init__(self, id_, first_name, last_name,
                 email, is_admin, date_created):
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.date_created = date_created
    def __str__(self):
        return (
            "{} {}:\n"
            "\temail: {}\n"
            "\tcreated on: {}"
            .format(self.first_name,
                    self.last_name,
                    self.email,
                    self.date_created)
        )

class Post:

    def __init__(self, id_, creator_id, body, date_created, thumbnail_url):
        self.id = id_
        self.creator_id = creator_id
        self.body = body
        self.date_created = date_created
        self.thumbnail_url = thumbnail_url

    def __str__(self):
        return self.body

class Event:

    def __init__(self, id_, event_name, event_description, date, location):
        self.id = id_
        self.event_name = event_name
        self.event_description = event_description
        self.date = date
        self.location = location

    def __str__(self):
        return self.event_name + ": " + self.event_description
