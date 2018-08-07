from db.dao import UserDAO

def get_current_user():
    try:
        id = current_user.id
        return current_user
    except:
        return None

def user(self):
    return UserDAO.get_user(self.creator_id).full_name()
