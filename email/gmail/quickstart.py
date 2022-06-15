from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os,sys
CLIENT_SECRET_FILE = 'email/gmail/client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

emailaddr = str(sys.argv[1])
emailtitle = str(sys.argv[2])
emailsmg = str(sys.argv[3])

emailaddr = str(emailaddr.replace('_', ' '))
emailtitle = str(emailtitle.replace('_', ' '))
emailsmg = str(emailsmg.replace('_', ' ').replace('+', '<br>'))

print(emailaddr)
print(emailtitle)
print(emailsmg)

emailMsg = emailsmg
mimeMessage = MIMEMultipart()
mimeMessage['to'] = emailaddr
mimeMessage['subject'] = emailtitle
mimeMessage.attach(MIMEText(emailMsg, 'html'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)