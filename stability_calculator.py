import pandas as pd
from db_connector import get_db_connection
from flask import jsonify
from datetime import datetime, timedelta
from helper import create_date_array, create_zeros_array, get_current_day, get_days_one_month, get_days_between

def getAllData(period):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if period == '3 DAY':
        query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks WHERE timestamp >= NOW() - INTERVAL 3 DAY ORDER BY sum"
    elif period == '1 WEEK':
        query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 WEEK ORDER BY sum"
    elif period == 'CUR_MONTH':
        query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks WHERE MONTH(`timestamp`) = MONTH(NOW()) ORDER BY sum"
    elif period == '1 MONTH':
        query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 MONTH ORDER BY sum"
    else:
        query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks ORDER BY sum"
        
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

    if period == '3 DAY':
        query = "SELECT keyword, AVG(sum) as average_revenue FROM postbacks WHERE timestamp >= NOW() - INTERVAL 3 DAY GROUP BY keyword ORDER BY average_revenue DESC;"
    elif period == '1 WEEK':
        query = "SELECT keyword, AVG(sum) as average_revenue FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 WEEK GROUP BY keyword ORDER BY average_revenue DESC;"
    elif period == 'CUR_MONTH':
        query = "SELECT keyword, AVG(sum) as average_revenue FROM postbacks WHERE MONTH(`timestamp`) = MONTH(NOW()) GROUP BY keyword ORDER BY average_revenue DESC;"
    elif period == '1 MONTH':
        query = "SELECT keyword, AVG(sum) as average_revenue FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 MONTH GROUP BY keyword ORDER BY average_revenue DESC;"
    else:
        query = "SELECT keyword, AVG(sum) as average_revenue FROM postbacks GROUP BY keyword ORDER BY average_revenue DESC;"
        
    cursor.execute(query)
    rows = cursor.fetchall()

    # Prepare data for chart
    
    data = {
        "keywords": [row[0] for row in rows],
        "average_revenues": [row[1] for row in rows]
    }
    
    print(data)

    cursor.close()
    conn.close()

    return jsonify(data)

def getKeywordList(period):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if period == '3 DAY':
        query = "SELECT keyword FROM postbacks WHERE timestamp >= NOW() - INTERVAL 3 DAY GROUP BY keyword "
    elif period == '1 WEEK':
        query = "SELECT keyword FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 WEEK GROUP BY keyword"
    elif period == 'CUR_MONTH':
        query = "SELECT keyword FROM postbacks WHERE MONTH(`timestamp`) = MONTH(NOW()) GROUP BY keyword"
    elif period == '1 MONTH':
        query = "SELECT keyword FROM postbacks WHERE timestamp >= NOW() - INTERVAL 1 MONTH GROUP BY keyword"
    else:
        query = "SELECT clickid, keyword, sum, relatedlink, timestamp, domain FROM postbacks ORDER BY sum"
        
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row.get('keyword'))
    cursor.close()
    conn.close()
    
    return result

def get_daily_chartData(keyword, period):
    conn = get_db_connection()
    cursor = conn.cursor()
    log_date_array = []
    
    if period == '3 DAY':
        query = "SELECT DATE(timestamp) as log_date, AVG(sum) as average_revenue FROM postbacks WHERE keyword = %s AND timestamp >= NOW() - INTERVAL 3 DAY GROUP BY DATE(`timestamp`) ORDER BY DATE(`timestamp`) ASC;"
        log_date_array = create_date_array(3)
    elif period == '1 WEEK':
        query = "SELECT DATE(timestamp) as log_date, AVG(sum) as average_revenue FROM postbacks WHERE keyword = %s AND timestamp >= NOW() - INTERVAL 1 WEEK GROUP BY DATE(`timestamp`) ORDER BY DATE(`timestamp`) ASC;"
        log_date_array = create_date_array(7)
    elif period == 'CUR_MONTH':
        query = "SELECT DATE(timestamp) as log_date, AVG(sum) as average_revenue FROM postbacks WHERE keyword = %s AND MONTH(`timestamp`) = MONTH(NOW()) GROUP BY DATE(`timestamp`) ORDER BY DATE(`timestamp`) ASC;"
        log_date_array = create_date_array(get_current_day(datetime.now()))
    elif period == '1 MONTH':
        query = "SELECT DATE(timestamp) as log_date, AVG(sum) as average_revenue FROM postbacks WHERE keyword = %s AND timestamp >= NOW() - INTERVAL 1 MONTH GROUP BY DATE(`timestamp`) ORDER BY DATE(`timestamp`) ASC;"
        log_date_array = create_date_array(get_days_one_month(datetime.now()))
    else:
        query = "SELECT DATE(timestamp) as log_date, AVG(sum) as average_revenue FROM postbacks WHERE keyword = %s GROUP BY DATE(`timestamp`) ORDER BY DATE(`timestamp`) ASC;"
        
    print(query, keyword, 'daily query')
    cursor.execute(query, (keyword, ))
    rows = cursor.fetchall()

    print(rows[0][0], "+++++++++++++++++++++")
    if period == "All":
        log_date_array = create_date_array(get_days_between(rows[0][0], datetime.now()))
    avg_revenue_array = create_zeros_array(len(log_date_array))
    print(log_date_array, 'log_date_array')
    # Prepare data for chart
    
    for index, item in enumerate(log_date_array):
        print(rows,'rows+++++++')
        for row in rows:
            print(item, row[0], item == row[0], type(item), type(str(row[0])), 'ppp')
            if item == str(row[0]):
                avg_revenue_array[index] = row[1]
                break

    data = {
        "log_dates": log_date_array,
        "average_revenues": avg_revenue_array
    }
    
    print(data, 'daily_chat_data')

    cursor.close()
    conn.close()

    return jsonify(data)