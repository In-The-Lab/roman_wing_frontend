def get_current_user():
    try:
        id = current_user.id
        return current_user
    except:
        return None
