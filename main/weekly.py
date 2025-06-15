import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta, datetime
from config import sender_email, sender_password, recipient_emails
import calendar
from datetime import datetime


def data_handler(data):
    data = data.rename(columns={'الإسم': 'name', 'تاريخ الميلاد': 'birthdate', 'رقم الولد': 'boy_number',
                                'رقم الأم': 'mom_number', 'رقم الأب': 'dad_number'})
    data = data[['name', 'birthdate', 'boy_number', 'mom_number', 'dad_number']]
    data['birthdate'] = pd.to_datetime(data['birthdate'], format='%d/%m/%Y')
    return data


def select_rows_last(data):
    today = datetime.now().date()
    seven_days_earlier = pd.Timestamp(today - timedelta(days=6))
    today = pd.Timestamp(today)
    selected_dates = pd.date_range(start=seven_days_earlier, end=today)
    selected_days = selected_dates.strftime('%d/%m').tolist()  # Extract day and month as strings
    
    # Filter rows based on 'birthdate' ignoring the year
    selected_rows = data[data['birthdate'].dt.strftime('%d/%m').isin(selected_days)].copy()

    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day
    return selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])


def select_rows_next(data):
    today = datetime.now().date()
    seven_days_later = pd.Timestamp(today + timedelta(days=7))
    today = pd.Timestamp(today)
    selected_dates = pd.date_range(start=today, end=seven_days_later)
    selected_days = selected_dates.strftime('%d/%m').tolist()  # Extract day and month as strings
    
    # Filter rows based on 'birthdate' ignoring the year
    selected_rows = data[data['birthdate'].dt.strftime('%d/%m').isin(selected_days)].copy()

    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day
    return selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])


def construct_mail(care_rows, today, body):
    if(len(care_rows['name'])==0):
        body += "-- Nobody --\n"
    else:
        for name in care_rows['name']:
            row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
            date_part = pd.Timestamp(row['birthdate']).date()
            birth_part = date_part.replace(year=today.year) # replacing birth year by this year, to get correct day of birth
            day_of_week = birth_part.weekday()
            day_name = calendar.day_name[day_of_week]
            date = row.birthdate.strftime('%d-%m-%Y')
            body += f"{day_name} {str(date)} --> {name}\n"
    return body

def construct_mail_last_week(rows, today):
    body = "Last week was the birthday of:\n"
    return construct_mail(rows, today, body)

def construct_mail_next_week(rows, today):
    body = "This week is the birthday of:\n"
    return construct_mail(rows, today, body)

def construct_final_mail(last_week, next_week, today):
    body_last = construct_mail_last_week(last_week, today)
    body_next = construct_mail_next_week(next_week, today)
    return body_last + "\n" + body_next


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
      print(f"body: {body}")
      send_email(subject, body, sender, password, recipients)
      print(f"email sent successfully to {recipients[1]}")
  else:
      print("No birthdays today.")



# CONSTANTS:
sheet_id = '1xO3JveyoACkecDP7dfs5Sk3FoKFCy64W'
sender = sender_email
password = sender_password
recipients = recipient_emails

# Storing Excel into df
data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
data = data_handler(data) # extracting relevant columns (5) and converting date format
last_week_rows = select_rows_last(data)
next_week_rows = select_rows_next(data)
care_rows = pd.concat([last_week_rows, next_week_rows])

body = construct_final_mail(last_week_rows, next_week_rows, datetime.now().date())
print(body) # Try it from cmd (VsCode doesn't support Arabic characters)

subject = "Week Birthdays!"
# send_mails(subject, body, sender, password, recipients, care_rows)

# # send_mails(subject_last, body_last, sender, password, recipients, last_week_rows)
# # send_mails(subject_next, body_next, sender, password, recipients, next_week_rows)


