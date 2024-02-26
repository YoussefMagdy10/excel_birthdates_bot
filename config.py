# /your_package/config.py
import os

def get_password(environ_string):
  try:
    sender_pass = os.environ[environ_string]
  except KeyError:
    sender_pass = "TOKEN NOT AVAILABLE!"
  return sender_pass


sender_email = 'abomakar.maximos.domadios@gmail.com'
sender_password = get_password("SENDER_PASS")

recipient_emails = [sender_email,
                    # 'georgemrafla@gmail.com',
                    # 'youssefmagdi1210@gmail.com',
                    # 'michaelashraf1234@gmail.com',
                    # 'pierregorgy@gmail.com',
                    # 'Anthony.IMEOR@gmail.com',
                    # 'Andrewwadie2000@gmail.com',
                    'georgetarek29@gmail.com'
                    ]
