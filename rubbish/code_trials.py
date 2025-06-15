import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta, datetime
import calendar
from datetime import datetime


def data_handler(data):
    data = data.rename(columns={'الإسم': 'name', 'تاريخ الميلاد': 'birthdate', 'رقم الولد': 'boy_number',
                                'رقم الأم': 'mom_number', 'رقم الأب': 'dad_number'})
    data = data[['name', 'birthdate', 'boy_number', 'mom_number', 'dad_number']]
    data['birthdate'] = pd.to_datetime(data['birthdate'], format='%d/%m/%Y')
    return data

# testing
def select_rows_last(data):
    today = datetime.now().date()
    seven_days_earlier = pd.Timestamp(today - timedelta(days=30))
    today = pd.Timestamp(today)
    selected_dates = pd.date_range(start=seven_days_earlier, end=today)
    selected_days = selected_dates.strftime('%d/%m').tolist()  # Extract day and month as strings
    
    # Filter rows based on 'birthdate' ignoring the year
    selected_rows = data[data['birthdate'].dt.strftime('%d/%m').isin(selected_days)]
    selected_rows = (selected_rows.sort_values(by='birthdate')).to_dict(orient='records')

    return selected_rows # List of dictionaries


def select_rows_next(data):
    today = datetime.now().date()
    seven_days_later = pd.Timestamp(today + timedelta(days=31))
    today = pd.Timestamp(today)
    selected_dates = pd.date_range(start=today, end=seven_days_later)
    selected_days = selected_dates.strftime('%d/%m').tolist()  # Extract day and month as strings
    
    # Filter rows based on 'birthdate' ignoring the year
    selected_rows = data[data['birthdate'].dt.strftime('%d/%m').isin(selected_days)]
    selected_rows = (selected_rows.sort_values(by='birthdate')).to_dict(orient='records')

    return selected_rows # List of dictionaries


# CONSTANTS:
sheet_id = '1xO3JveyoACkecDP7dfs5Sk3FoKFCy64W'
# sender = sender_email
# password = sender_password
# recipients = recipient_emails

# Storing Excel into df
data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
data = data_handler(data) # extracting relevant columns (5) and converting date format
last_week = select_rows_last(data)
next_week = select_rows_next(data)
# Example usage:
print("Last Month's birthdays:")
for row in last_week:
    print(f"{row['name']} - {row['birthdate'].strftime('%d/%m')}")
print("Next Month's birthdays:")
for row in next_week:
    print(f"{row['name']} - {row['birthdate'].strftime('%d/%m')}")
# print(last_week_rows)

# next_week_rows, today = select_rows_next(data)
# care_rows = pd.concat([last_week_rows, next_week_rows])
