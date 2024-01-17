import pandas as pd
from db_connector import get_db_connection
from flask import jsonify

def getAllData(period):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 MONTH ORDER BY sum"

    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
       temp=[]
       for item in row:
          temp.append(row.get(item))
       result.append(temp)
    cursor.close()
    conn.close()
    
    return result
 
def calculate_stability_for_chart(period):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT clickid, keyword, AVG(sum) as average_revenue FROM postbacks GROUP BY clickid"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Prepare data for chart
    data = {
        "clickids": [row[0] for row in rows],
        "keywords": [row[1] for row in rows],
        "average_revenues": [row[2] for row in rows]
    }
    
    print(data)

    cursor.close()
    conn.close()

    return jsonify(data)
