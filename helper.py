from datetime import datetime, timedelta

def create_date_array(days):
   dates = []
   today = datetime.now()

   for i in range(days):
      date = today - timedelta(days=i)
      dates.append(date.strftime('%Y-%m-%d'))

   dates.reverse()
   return dates

def create_zeros_array(length):
   temp = []
   for i in range(length):
      temp.append(0)
   return temp

def get_current_day(date):
   return date.day

def get_days_one_month(current_date):
   # Calculate the first day of the current month
   first_day_of_current_month = current_date.replace(day=1)

   # Calculate the last day of the previous month
   last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
   same_day_of_previous_month = last_day_of_previous_month.replace(day=current_date.day)
   # Calculate the number of days from today to the same day of the previous month
   days_difference = (current_date - same_day_of_previous_month).days+1
   return days_difference

def get_days_between(from_date, to_date):
   # Calculate the first day of the current month
   days_difference = (to_date.date() - from_date).days+1
   return days_difference