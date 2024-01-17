import pymysql
from db_connector import get_db_connection

def insert_postback_data(clickid, sum, relatedlink, timestamp, domain, keyword):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO postbacks (clickid, sum, relatedlink, timestamp, domain, keyword) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (clickid, sum, relatedlink, timestamp, domain, keyword))
        connection.commit()
    finally:
        connection.close()