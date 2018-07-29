from mysql.connector import connection, Error
try:
    from .migrations import tables
except:
    from migrations import tables
import configparser
import sys

def get_db_config():
    config = configparser.ConfigParser()
    config.read("../config/config.ini")
    user = config["MYSQL"]["user"]
    pword = config["MYSQL"]["password"]
    host = config["MYSQL"]["host"]
    db = config["MYSQL"]["database"]
    return user, pword, host, db

def get_db_connection(user, pword, host, db, clean=False):
    if not clean:
        cnx = connection.MySQLConnection(user=user,
                                         password=pword,
                                         host=host,
                                         database=db)
    else:
        cnx = connection.MySQLConnection(user=user,
                                         password=pword,
                                         host=host)
    cursor = cnx.cursor()
    return cnx, cursor

def clean_database():
    '''
        WARNING:
        ALL DATA IN THE DATABASE WILL BE WIPED
        WHEN THIS COMMAND IS CALLED. BE WARNED.
    '''
    db = get_db_config()[3] # need db name
    cnx, cursor = get_db_connection(*get_db_config(), clean=True)
    cursor.execute("DROP DATABASE `{}`".format(db))
    cursor.execute("CREATE DATABASE `{}`".format(db))

def apply_migration():
    cnx, cursor = get_db_connection(*get_db_config())
    for table_name in tables.keys():
        cmd = tables[table_name]
        print("Creating table " + table_name + "...")
        try:
            cursor.execute(cmd)
        except Error as err:
            print(err)
        else:
            print("Created table " + table_name)

if __name__ == "__main__":
    migrate = False
    clean = False
    if len(sys.argv) >= 2:
        if "--migrate" in sys.argv:
            migrate = True
        if "--clean" in sys.argv:
            clean = True
        if "--migrate" not in sys.argv and "--clean" not in sys.argv:
            print("Usage: \"python dbutils.py [--migrate] [--clean]\"")
            exit()
    else:
        print("Usage: \"python dbutils.py [--migrate] [--clean]\"")
        exit()
    if clean:
        clean_database()
    if migrate:
        apply_migration()
