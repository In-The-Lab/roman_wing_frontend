from mysql.connector import connection, Error
import bcrypt
from models import User
from dao import UserDAO, AuthDAO
import configparser

usrs = [
    (("Will", "Cravitz", "wcravitz@lsoc.org"), ("pass")),
    (("Vedant", "Pathak", "vpathak@lsoc.org"), ("pass")),
]

for usr, pass_ in usrs:
    UserDAO.insert_user(usr[0], usr[1], usr[2])
    id = UserDAO.get_user_by_email(usr[2])
    AuthDAO.insert_hash(bcrypt.hashpw(id, pass_.encode("utf-8")))
