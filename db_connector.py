import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',        # your host, usually localhost
        user='root',     # your MySQL username
        passwd='',   # your MySQL password
        db='keywords'          # name of the data base
    )
    return connection
