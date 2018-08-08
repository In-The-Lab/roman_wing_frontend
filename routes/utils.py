from flask_login import current_user
from db.dao import UserDAO, PostDAO, EventDAO

def get_current_user():
    try:
        id = current_user.id
        return current_user
    except:
        return None

def user(self):
    return UserDAO.get_user(self.creator_id).full_name()

def collect_from_db_for_index():
    articles = PostDAO.get_approved_posts()
    articles.sort(key=lambda p: p.date_created, reverse=True)
    events = EventDAO.get_all_future_events()
    if len(articles) > 10:
        articles = articles[:10]
    return articles, events
