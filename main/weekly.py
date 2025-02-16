import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta, datetime
from config import sender_email, sender_password, recipient_emails
import calendar
from datetime import datetime
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


def select_rows_last(data):
    today = datetime.now().date()
    seven_days_earlier = today - timedelta(days=7)
    seven_days_earlier = pd.Timestamp(seven_days_earlier)
    today = pd.Timestamp(today)

    selected_rows_1 = data[
        (data['birthdate'].dt.month == today.month) &  # Check month
        (data['birthdate'].dt.day < today.day)
    ]  # Check day < today
    # Apply additional filtering only if the previous condition is met (day < today)
    if today.day > seven_days_earlier.day:
        selected_rows_1 = selected_rows_1[
            selected_rows_1['birthdate'].dt.day > seven_days_earlier.day
        ]

    selected_rows_2 = pd.DataFrame(columns=data.columns)
    
    if seven_days_earlier.month == today.month - 1:
        selected_rows_2 = data[
            (data['birthdate'].dt.month == today.month - 1) & 
            (data['birthdate'].dt.day <= calendar.monthrange(today.year, today.month - 1)[1]) & 
            (data['birthdate'].dt.day > seven_days_earlier.day)
        ]

    # Concatenate selected rows
    selected_rows = pd.concat([selected_rows_1, selected_rows_2])

    # Ensure 'birthdate' is in datetime format
    selected_rows['birthdate'] = pd.to_datetime(selected_rows['birthdate'])

    # Extract month and day
    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day

    selected_rows = selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])
    return selected_rows, today


def select_rows_next(data):
    today = datetime.now().date()
    seven_days_later = today + timedelta(days=7)  # Calculate date 7 days later
    seven_days_later = pd.Timestamp(seven_days_later)
    today = pd.Timestamp(today)
    # print(today)

    # Filter rows for birthdays within the next 7 days (inclusive)
    data['birthdate'] = pd.to_datetime(data['birthdate'])

    # Get today's date
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    seven_days_later = today + timedelta(days=7)

    # Filter birthdays occurring within the next 7 days
    selected_rows = data[
        ((data['birthdate'].dt.month == tomorrow.month) & (data['birthdate'].dt.day >= tomorrow.day)) |
        ((data['birthdate'].dt.month == seven_days_later.month) & (data['birthdate'].dt.day <= seven_days_later.day))
    ]

    # Extract month and day
    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day

    # Sort by month and day
    selected_rows = selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])

    # Drop the temporary columns if you don't need them anymore
    selected_rows = selected_rows.drop(columns=['month', 'day'])
    return selected_rows, today


def construct_mail_last(care_rows, today):
    # subject = f'أعياد ميلاد الأسبوع الماضي - ما بين: {(today - timedelta(days=7)).strftime("%Y-%m-%d")} & {today.strftime("%Y-%m-%d")}'
    body = "Last week was the birthday of:\n"
    if(len(care_rows['name'])==0):
        body += "-- Nobody --\n"
    for name in care_rows['name']:
        row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
        date_part = pd.Timestamp(row['birthdate']).date()
        birth_part = date_part.replace(year=today.year) # replacing birth year by this year, to get correct day of birth
        day_of_week = birth_part.weekday()
        day_name = calendar.day_name[day_of_week]
        date = row.birthdate.strftime('%d-%m-%Y')
        body += f"{day_name} {str(date)} --> {name}\n"

    return body

def construct_mail_next(care_rows, today):
    # subject = f'أعياد ميلاد الأسبوع القادم - ما بين: {today.strftime("%d-%m-%Y")} & {(today + timedelta(days=7)).strftime("%d-%m-%Y")}'

    body = "This week is the birthday of:\n"
    if(len(care_rows['name'])==0):
        body += "-- No one --\n"
    for name in care_rows['name']:
        row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
        date_part = pd.Timestamp(row['birthdate']).date()
        birth_part = date_part.replace(year=today.year) # replacing birth year by this year, to get correct day of birth
        day_of_week = birth_part.weekday()
        day_name = calendar.day_name[day_of_week]
        date = row.birthdate.strftime('%d-%m-%Y')
        body += f"{day_name} {str(date)} --> {name}\n"

    return body



# CONSTANTS:
sheet_id = '1xO3JveyoACkecDP7dfs5Sk3FoKFCy64W'
sender = sender_email
password = sender_password
recipients = recipient_emails

# Storing Excel into df
data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
data = data_handler(data)
last_week_rows, _ = select_rows_last(data)
next_week_rows, today = select_rows_next(data)
care_rows = pd.concat([last_week_rows, next_week_rows])


body_last = construct_mail_last(last_week_rows, today)
body_next = construct_mail_next(next_week_rows, today)

final_body = body_last + "\n" + body_next

subject = "Week Birthdays!"
send_mails(subject, final_body, sender, password, recipients, care_rows)

# send_mails(subject_last, body_last, sender, password, recipients, last_week_rows)
# send_mails(subject_next, body_next, sender, password, recipients, next_week_rows)


