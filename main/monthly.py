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
      # print(f"body: {body}")
      send_email(subject, body, sender, password, recipients)
      # print(f"email sent successfully to {recipients[1]}")
  else:
      print("No birthdays today.")


def data_handler(data):
    data = data.rename(columns={'الإسم': 'name', 'تاريخ الميلاد': 'birthdate', 'رقم الولد': 'boy_number',
                                'رقم الأم': 'mom_number', 'رقم الأب': 'dad_number'})
    data = data[['name', 'birthdate', 'boy_number', 'mom_number', 'dad_number']]
    data['birthdate'] = pd.to_datetime(data['birthdate'], format='%d/%m/%Y')
    return data

def select_rows(data):
    today = datetime.now().date()
    today = pd.to_datetime(today)
    # Filter rows for birthdays within the next 7 days (inclusive)
    selected_rows = data[
        (data['birthdate'].dt.month == today.month)
    ]

    # Extract month and day
    selected_rows['month'] = selected_rows['birthdate'].dt.month
    selected_rows['day'] = selected_rows['birthdate'].dt.day

    selected_rows = selected_rows.sort_values(by=['month', 'day'], ascending=[True, True])
    return selected_rows, today


def construct_mail(care_rows, today):
    subject = f'أعياد ميلاد شهر {today.month}'

    # body = "Welcome O Andrew to our births bot 😄. Here is how it works:\nEvery month's birthdays are emailed on the first day of each month @ 10AM. \nEvery Friday, the birthdays of the upcoming week (& those of the previous one in case you missed any) are emailed @ 10AM. Finally, whenever there is a birthday on a day, it's emailed @ 7AM.\nEnjoy your stay 😍\n\nBelow, you can find a sample of our Monthly email. Unfortunately, this month has only 1 birthday!\n     ↓↓↓↓↓\n\nThis month is the birthday of:\n"
    body = "This month is the birthday of:\n"
    for name in care_rows['name']:
        row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
        date_part = pd.Timestamp(row['birthdate']).date()
        birth_part = date_part.replace(year=today.year) # replacing birth year by this year, to get correct day of birth
        day_of_week = birth_part.weekday()
        day_name = calendar.day_name[day_of_week]
        date = row.birthdate.strftime('%d-%m-%Y')
        body += f"{day_name} {str(date)} --> {name}\n"

    # body += "🔴🔴🔴If this works for you, please DM me on WhatsApp confirming that you received this email.🔴🔴🔴"
    # body += "Later, you will receive: \n"
    # body += "- A list of the birthdays on the 1st day of the each month at 10:00AM.\n"
    # body += "- A list of next week's birthdays on Sundays at 10:00AM (containing the next 8 days inclusive: from Sunday to Sunday).\n"
    # body += "- The birthday of the day at 7:00AM (If there is any).\n"
    # body += "Enjoy your day :)"
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
care_rows, today = select_rows(data)
subject, body = construct_mail(care_rows, today)

# send_mails(subject_last, body_last, sender, password, recipients, last_week_rows)
send_mails(subject, body, sender, password, recipients, care_rows)
