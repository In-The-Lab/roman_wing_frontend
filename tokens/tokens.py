import configparser
import jwt

'''
    You pretty much only need a token to update
    your own information and make posts. Tokens
    are also used to determine whether a user is
    an admin or not.
'''

def get_jwt_secret():
    config = configparser.ConfigParser()
    config.read("../config/config.ini")
    return config["JWT"]["secret"]

def create_user_token(id_, is_admin):
    scrt = get_jwt_secret()
    pld = {"id": id_, "is_admin": is_admin}
    return jwt.encode(pld, scrt, algorithm="HS256")

def get_id_from_token(tok):
    scrt = get_jwt_secret()
    pld = jwt.decode(tok, scrt, algorithms=["HS256"])
    return pld["id"]

def is_admin(tok):
    scrt = get_jwt_secret()
    return jwt.decode(tok, scrt, algorithms["HS256"])["is_admin"]