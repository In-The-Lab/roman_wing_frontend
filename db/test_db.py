from mysql.connector import connection, Error
import configparser

config = configparser.ConfigParser()
print("Loading config.ini...")
try:
    config.read("config.ini")
except:
    print("config.ini not found.")
    exit()

print("Connecting to database...")
try:
    cnx = connection.MySQLConnection(user=config["MYSQL"]["user"],
                                     password=config["MYSQL"]["password"],
                                     host=config["MYSQL"]["host"],
                                     database=config["MYSQL"]["database"])
    print("All connected!")
except Error as err:
    print(err)