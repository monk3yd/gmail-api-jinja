import os.path

# Gmail API utils
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
# from mimetypes import guess_type as guess_mime_type

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send'
]

# Connect to Gmail's API (Authentication)
def gmail_authenticate():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def open_template(template_path):
    with open(template_path, "r") as file:
        template = file.read()
        return template

# Create a message for an email. returns an object contaianing base64url encoded email objects.
def create_message(sender, receiver, subject, html, text):
    message = MIMEMultipart('alternative')
    message['sender'] = sender
    message['receiver'] = receiver
    message['subject'] = subject

    plain_msg_body = MIMEText(text, 'plain')
    html_msg_body = MIMEText(html, 'html')

    message.attach(plain_msg_body)
    message.attach(html_msg_body)

    print(message.as_string())

    # 1.2 and encode it as a base64url string.
    return {'raw': urlsafe_b64encode(message.as_string().encode())}