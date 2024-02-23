import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
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

def data_handler(data):
    data = data.rename(columns={'الإسم': 'name', 'تاريخ الميلاد': 'birthdate', 'رقم الولد': 'boy_number', 
                                'رقم الأم': 'mom_number', 'رقم الأب': 'dad_number'})
    data = data[['name', 'birthdate', 'boy_number', 'mom_number', 'dad_number']]
    data['birthdate'] = pd.to_datetime(data['birthdate'], format='%d/%m/%Y')


def select_rows(data): # specific to daily.py code
  today = datetime.now().date()
  return data[(data['birthdate'].dt.day == today.day) & (data['birthdate'].dt.month == today.month)], today

def construct_mail(care_rows, today): # specific to daily.py code
  subject = f'أعياد ميلاد {today}'

  body = f'Today is the birthday of:\n\n'
  for name in care_rows['name']:
    row = care_rows.loc[care_rows['name'] == name].squeeze() # attributes: name, birthdate, boy_number, mom_number, dad_number
    age = int(today.year - row.birthdate.year)
    body += f"{name}, he is now {age} years old!\n"
    body += f"Wish him a happy birthday :) \nContact phone numbers:\n"
    if row.boy_number != 'NaN':
      boy_name = name.split()[0]
      body += f"{boy_name}: {row.boy_number}\n"
    if row.mom_number != 'NaN':
      body += f"Mother: {row.mom_number}\n"
    if row.dad_number != 'NaN':
      body += f"Father: {row.dad_number}\n"
    body += "\n"
    
  return subject, body

def send_mails(subject, body, sender, password, recipients, care_rows): # to be exported
  if not care_rows.empty:  # send emails to 5odam!
      print("People with birthdays today:")
      print(care_rows['name'].tolist())
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
data = data_handler(data)
care_rows, today = select_rows(data)
subject, body = construct_mail(care_rows, today)

send_mails(subject, body, sender, password, recipients, care_rows)

print(f"mail sent successfully to {recipients}!")