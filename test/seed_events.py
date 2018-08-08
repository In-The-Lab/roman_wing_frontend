from db.dbutils import get_db_config, get_db_connection

cnx, cursor = get_db_connection(*get_db_config())
url = "https://i.kym-cdn.com/entries/icons/mobile/000/013/564/doge.jpg"

cmd = (
    "INSERT INTO users "
    "(first_name, last_name, email, is_admin, date_created) "
    "VALUES (\'sample\', \'admin\', \'sample@admin.com\', "
    "TRUE, CURDATE())"
)
cursor.execute(cmd)
cnx.commit()

for i in range(20):
    str_ = "seed post {}".format(i)
    cmd = (
        "INSERT INTO posts "
        "(creator_id, title, description, body, date_created, "
        "thumbnail_url, is_authorized) "
        "VALUES ({}, \'{}\', \'{}\', \'{}\', CURDATE(), \'{}\', TRUE)"
        .format(1, str_, str_, str_, url)
    )
    cursor.execute(cmd)
    cnx.commit()
