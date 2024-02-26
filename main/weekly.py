import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta, datetime
from config import sender_email, sender_password, recipient_emails
import os


def send_email(subject, body, sender, password, recipients): # to be exported
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

def send_mails(subject, body, sender, password, recipients, care_rows): # to be exported
  if not care_rows.empty:  # send emails to 5odam!
      # print("People with birthdays today:")
      # print(care_rows['name'].tolist())
      print(f"body: {body}")
      send_email(subject, body, sender, password, recipients)
      print(f"email sent successfully to {recipients[1]}")
  else:
      print("No birthdays today.")

def data_handler(data):
    data = data.rename(columns={'الإسم': 'name', 'تاريخ الميلاد': 'birthdate', 'رقم الولد': 'boy_number', 
                                'رقم الأم': 'mom_number', 'رقم الأب': 'dad_number'})
    data = data[['name', 'birthdate', 'boy_number', 'mom_number', 'dad_number']]
    data['birthdate'] = pd.to_datetime(data['birthdate'], format='%d/%m/%Y')
    return data

# def select_rows_last(data): # --> Needs logic revision
#     today = datetime.now().date()
#     seven_days_ago = today - timedelta(days=7)  # Calculate date 7 days ago
#     seven_days_ago = pd.Timestamp(seven_days_ago)

#     today = pd.to_datetime(today)
#     # Filter rows for birthdays within the last 7 days (inclusive)
#     selected_rows = data[
#         ((data['birthdate'].dt.month == seven_days_ago.month) & (data['birthdate'].dt.day >= seven_days_ago.day) & (data['birthdate'].dt.day <= today.day)) |
#         ((today.month - data['birthdate'].dt.month == 1) & (data['birthdate'].dt.day > today.day + 21))
#     ]
#     return selected_rows, today

def select_rows_next(data):
    today = datetime.now().date()
    seven_days_later = today + timedelta(days=7)  # Calculate date 7 days later
    seven_days_later = pd.Timestamp(seven_days_later)

    today = pd.to_datetime(today)
    # Filter rows for birthdays within the next 7 days (inclusive)
    selected_rows = data[
        ((data['birthdate'].dt.month == today.month) & (data['birthdate'].dt.day <= seven_days_later.day) & data['birthdate'].dt.day > today.day) | 
        ((data['birthdate'].dt.month - today.month == 1) & (data['birthdate'].dt.day <= seven_days_later.day))
    ]
    return selected_rows, today

def construct_mail_last(care_rows, today):
    subject = f'أعياد ميلاد الأسبوع الماضي - ما بين: {(today - timedelta(days=7)).strftime("%Y-%m-%d")} & {today.strftime("%Y-%m-%d")}'
    
    body = "Last week was the birthday of:\n"
    for name in care_rows['name']:
        row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
        date = row.birthdate.strftime('%Y-%m-%d')
        body += f"{str(date)} --> {name}\n"

    return subject, body

def construct_mail_next(care_rows, today):
    subject = f'أعياد ميلاد الأسبوع القادم - ما بين: {today.strftime("%Y-%m-%d")} & {(today + timedelta(days=7)).strftime("%Y-%m-%d")}'

    body = "This week is the birthday of:\n"
    for name in care_rows['name']:
        row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
        date = row.birthdate.strftime('%Y-%m-%d')
        body += f"{str(date)} --> {name}\n"

    return subject, body


# CONSTANTS:
sheet_id = '1xO3JveyoACkecDP7dfs5Sk3FoKFCy64W'
sender = sender_email
password = sender_password
recipients = recipient_emails

# Storing Excel into df
data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
data = data_handler(data)
# last_week_rows, _ = select_rows_last(data)
next_week_rows, today = select_rows_next(data)

# subject_last, body_last = construct_mail_last(last_week_rows, today)
subject_next, body_next = construct_mail_next(next_week_rows, today)

# send_mails(subject_last, body_last, sender, password, recipients, last_week_rows)
send_mails(subject_next, body_next, sender, password, recipients, next_week_rows)

