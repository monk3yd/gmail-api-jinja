import os.path
import urllib.parse

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
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from jinja2 import Template

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send'
]

# Stores all encoded messages
all_messages = []


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


def create_pixelURL_tracker(google_tracker):
    tracking_id = google_tracker['tracking_id']
    client_id = int(google_tracker['client_id'])
    anonymize_ip = int(google_tracker['anonymize_ip'])
    tracker_path = urllib.parse.quote(google_tracker['tracker_path'], safe='')
    tracker_title = urllib.parse.quote(google_tracker['tracker_title'], safe='')
    return f'https://www.google-analytics.com/collect?v=1&tid={tracking_id}&cid={client_id}&aip={anonymize_ip}&t=event&ec=email&ea=open&dp={tracker_path}&dt={tracker_title}'


def create_message(sender, receiver, subject, html, text):
    message = MIMEMultipart('alternative')
    message['from'] = sender
    message['to'] = receiver
    message['subject'] = subject

    message.attach(MIMEText(text, 'plain'))
    message.attach(MIMEText(html, 'html'))

    return {'raw': urlsafe_b64encode(message.as_bytes())}


# def create_message_with_attachment(sender, receiver, subject, html, file):
    # message = MIMEMultipart()
    # message['from'] = sender
    # message['to'] = receiver
    # message['subject'] = subject

    # message.attach(MIMEText(html, 'html'))

    # content_type, encoding = guess_mime_type(file)

    # if content_type is None or encoding is not None:
    #     content_type = 'application/octet-stream'

    # main_type, sub_type = content_type.split('/', 1)
    # if main_type == 'text':
    #     fp = open(file, 'rb')
    #     msg = MIMEText(fp.read(), _subtype=sub_type)
    #     fp.close()
    # elif main_type == 'image':
    #     fp = open(file, 'rb')
    #     msg = MIMEImage(fp.read(), _subtype=sub_type)
    #     fp.close()
    # elif main_type == 'audio':
    #     fp = open(file, 'rb')
    #     msg = MIMEAudio(fp.read(), _subtype=sub_type)
    #     fp.close()
    # else:
    #     fp = open(file, 'rb')
    #     msg = MIMEBase(main_type, sub_type)
    #     msg.set_payload(fp.read())
    #     fp.close()

    # filename = os.path.basename(file)
    # msg.add_header('Content-Disposition', 'attachment', filename=filename)
    # message.attach(msg)

    # return {'raw': base64.urlsafe_b64encode(message.as_bytes())}


def create_all_messages(sender, subject, parameters, pixelURL_tracker, html_text, no_html_text):
    # Loop through all receivers creating one message for each
    for user in parameters:
        email = user['email']
        name = user['name']
        age = str(user['age'])

        # TODO make function template_and_render(string, params)
        # Templating HTML with params and pixelURL variables  
        html_tm = Template(html_text)
        html = html_tm.render(
            name=name,
            age=age,
            pixelURL_tracker=pixelURL_tracker
        )  # kwargs**  ?? TODO render automatically?

        no_html_tm = Template(no_html_text)
        no_html = no_html_tm.render(name=name, age=age)  # A real no_html email can't be tracked. Need hybrid email. 

        # Create message
        encoded_message = create_message(sender, email, subject, html, no_html) 
        all_messages.append(encoded_message)
    return all_messages


def send_message(service, user_id, message):
    try:
        message['raw'] = message['raw'].decode()
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f'Message Id: {message["id"]}') 
        return message
    except HttpError as error:
        # (developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        return "Error"

# The high-level workflow to send an email is to:
    # 1.1 Create the email content

    # 1.2 and encode it as a base64url string.

    # 2.1 Create a new message resource

    # 2.2 and set its raw property to the base64url string you just created.

    # 3. Call messages.send, or, if sending a draft, drafts.send to send the message.