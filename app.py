from flask import Flask, render_template, request, jsonify
from stability_calculator import calculate_stability_for_chart, getAllData, getKeywordList, get_daily_chartData
from data_processor import insert_postback_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/postback', methods=['GET'])
def postback():
   try:
      clickid = request.args.get('clickid')
      sum = request.args.get('sum')
      relatedlink = request.args.get('sub20')
      timestamp = request.args.get('sub19')
      domain = request.args.get('sub18')
      keyword = request.args.get('keyword')

      # Insert the data into the database
      insert_postback_data(clickid, sum, relatedlink, timestamp, domain, keyword)

      return 'OK', 200

   except Exception as e:
      # Log the exception for debugging
      print(f"An error occurred: {e}")

      # Optionally, you could return a different response indicating an error
      return 'Error occurred', 500

@app.route('/report', methods=['GET'])
def report():
   period = request.args.get('period', '7 days')
   results = getAllData(period)
   return results
 
@app.route('/keywordlist', methods=['GET'])
def keywordlist():
   period = request.args.get('period', '7 days')
   results = getKeywordList(period)
   return results

@app.route('/chart-data', methods=['GET'])
def chart_data():
   period = request.args.get('period', '7 days')
   results = calculate_stability_for_chart(period)
   return results

@app.route('/daily-chart-data', methods=['GET'])
def daily_chart_data():
   period = request.args.get('period', '7 days')
   keyword = request.args.get('keyword', 'Développement D Applications Mobiles')
   results = get_daily_chartData(keyword, period)
   return results
 
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)
 
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)
