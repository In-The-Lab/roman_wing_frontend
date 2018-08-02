try:
    from .dbutils import get_db_config, get_db_connection
except:
    from dbutils import get_db_config, get_db_connection
try:
    from .models import User, Post, Event
except:
    from models import User, Post, Event

class UserDAO:

    @staticmethod
    def insert_user(first_name, last_name, email):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "INSERT INTO users "
            "(first_name, last_name, email, is_admin, date_created) "
            "VALUES (\'{}\', \'{}\', \'{}\', "
            "FALSE, CURDATE())".format(first_name,
                                       last_name,
                                       email))
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def get_user(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cursor.execute(("SELECT "
                        "id, first_name, last_name, email, is_admin, date_created "
                        "FROM users "
                        "WHERE id={}".format(id_)))
        usrs = []
        for (id__, first_name, last_name, email, is_admin, date_created) in cursor:
            usr = User(id__, first_name, last_name, email,
                             is_admin, date_created)
            usrs.append(usr)
        if len(usrs) == 0:
            return None
        return usrs[0]

    @staticmethod
    def get_user_by_email(email):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (("SELECT "
                "id, first_name, last_name, email, is_admin, date_created "
                "FROM users "
                "WHERE email=\'{}\'".format(email)))
        cursor.execute(cmd)
        usrs = []
        for (id_, first_name, last_name, email, is_admin, date_created) in cursor:
            usr = User(id_, first_name, last_name, email,
                             is_admin, date_created)
            usrs.append(usr)
        if len(usrs) == 0:
            return None
        return usrs[0]

    @staticmethod
    def update_user(id_, first_name, last_name, email):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "UPDATE users SET"
            "first_name=\'{}\', last_name=\'{}\', "
            "email=\'{}\'"
            "WHERE id={}".format(first_name, last_name, email, id_))
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def get_posts(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (("SELECT "
                "id, creator_id, body, date_created, thumbnail_url "
                "FROM posts "
                "WHERE creator_id={}".format(id_)))
        cursor.execute(cmd)
        posts = []
        for (id__, creator_id, body, date_created, thumbnail_url) in cursor:
            post = Post(id__, creator_id, body, date_created, thumbnail_url)
            posts.append(post)
        return posts

    @staticmethod
    def get_saved_posts(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "SELECT "
            "posts.id, posts.creator_id, posts.body, "
            "posts.date_created, posts.thumbnail_url "
            "FROM saved_articles "
            "INNER JOIN posts ON saved_articles.post_id=posts.id "
            "WHERE saved_articles.user_id={}".format(id_))
        cursor.execute(cmd)
        posts = []
        for (id__, creator_id, body, date_created, thumbnail_url) in cursor:
            post = Post(id__, creator_id, body, date_created, thumbnail_url)
            posts.append(post)
        return posts

class PostDAO:

    @staticmethod
    def insert_post(creator_id, title, desc, body, thumbnail_url):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "INSERT INTO posts "
            "(creator_id, title, description, body, date_created, "
            "thumbnail_url, is_authorized) "
            "VALUES ({}, \'{}\', \'{}\', \'{}\', CURDATE(), \'{}\', FALSE)"
            .format(creator_id, title, desc, body, thumbnail_url))
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def authorize_post(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "UPDATE posts SET "
            "is_authorized=TRUE "
            "WHERE id={}".format(id_)
        )
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def get_post(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "SELECT id, creator_id, title, description, body, date_created, "
            "thumbnail_url, is_authorized "
            "FROM posts WHERE id={}".format(id_))
        cursor.execute(cmd)
        posts = []
        for (id__, creator_id, title, description,
             body, date_created, thumbnail_url, is_authorized) in cursor:
            post = Post(id__, creator_id, title, description,
                        body, date_created, thumbnail_url, is_authorized)
            posts.append(post)
        return posts[0]

    @staticmethod
    def get_all_posts():
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "SELECT id, creator_id, title, description, body, date_created, "
            "thumbnail_url, is_authorized "
            "FROM posts")
        cursor.execute(cmd)
        posts = []
        for (id_, creator_id, title, description,
             body, date_created, thumbnail_url, is_authorized) in cursor:
            post = Post(id_, creator_id, title, description,
                        body, date_created, thumbnail_url, is_authorized)
            posts.append(post)
        return posts

    @staticmethod
    def get_unapproved_posts():
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "SELECT id, creator_id, title, description, body, date_created, "
            "thumbnail_url, is_authorized "
            "FROM posts WHERE is_authorized=FALSE")
        cursor.execute(cmd)
        posts = []
        for (id_, creator_id, title, description,
             body, date_created, thumbnail_url, is_authorized) in cursor:
            post = Post(id_, creator_id, title, description,
                        body, date_created, thumbnail_url, is_authorized)
            posts.append(post)
        return posts

    @staticmethod
    def get_approved_posts():
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "SELECT id, creator_id, title, description, body, date_created, "
            "thumbnail_url, is_authorized "
            "FROM posts WHERE is_authorized=TRUE")
        cursor.execute(cmd)
        posts = []
        for (id_, creator_id, title, description,
             body, date_created, thumbnail_url, is_authorized) in cursor:
            post = Post(id_, creator_id, title, description,
                        body, date_created, thumbnail_url, is_authorized)
            posts.append(post)
        return posts

    @staticmethod
    def delete_post(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = "DELETE FROM posts WHERE id={}".format(id_)
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def update_post_text(id_, updated_text):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "UPDATE posts SET body=\'{}\' WHERE id={}".format(updated_text, id_)
        )
        cursor.execute(cmd)
        cnx.commit()

class EventDAO:

    @staticmethod
    def create_event(name, description, date, location):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "INSERT INTO events "
            "(event_name, event_description, date, location) "
            "VALUES (\'{}\', \'{}\', "
            "STR_TO_DATE(\'{}\', \'%Y-%m-%d\'), \'{}\')"
            .format(name, description, date, location))
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def get_event(id_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "SELECT id, event_name, event_description, date, location "
            "FROM events WHERE id={}".format(id_))
        cursor.execute(cmd)
        events = []
        for (id_, event_name, event_description, date, location) in cursor:
            event = Event(id_, event_name, event_description, date, location)
            events.append(event)
        return events[0]

    @staticmethod
    def get_all_future_events():
        cnx, cursor = get_db_connection(*get_db_config())
        cmd  = (
            "SELECT id, event_name, event_description, date, location "
            "FROM events WHERE date>CURDATE()")
        cursor.execute(cmd)
        events = []
        for (id_, event_name, event_description, date, location) in cursor:
            event = Event(id_, event_name, event_description, date, location)
            events.append(event)
        return events

class AuthDAO:

    @staticmethod
    def insert_hash(user_id, hash_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "INSERT INTO user_auth "
            "(hash, user_id) "
            "VALUES (\'{}\', \'{}\')".format(hash_.decode('utf8'), user_id))
        print(cmd)
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def update_hash(user_id, hash_):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = (
            "UPDATE user_auth SET "
            "hash=\'{}\', user_id=\'{}\' "
            "WHERE user_id={}".format(hash_.decode('utf8'), user_id)
            )
        print(cmd)
        cursor.execute(cmd)
        cnx.commit()

    @staticmethod
    def get_hash(user_id):
        cnx, cursor = get_db_connection(*get_db_config())
        cmd = "SELECT hash from user_auth WHERE user_id={}".format(user_id)
        print(cmd)
        cursor.execute(cmd)
        hashes = []
        for (hash_) in cursor:
            print(hash_)
            hashes.append(hash_)
        return hashes[0][0].encode('utf-8')
