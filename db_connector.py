import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='66.29.130.114',        # your host, usually localhost
        user='root',     # your MySQL username
        passwd='iamattila01A!',   # your MySQL password
        db='keywords'          # name of the data base
    )
    return connection
