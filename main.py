# Project: Send Email via Gmail API (business) with Templates (jinja2) using Python

from __future__ import print_function

from pathlib import Path

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Own module
from utils import gmail_authenticate, open_template
# from objects import Email


class Email():
    def __init__(self, receivers, subject, template, parameters={}, no_html_template="", google_tracker={}):
        # Email Object Properties
        self.receivers = receivers
        self.subject = subject
        self.template = template
        self.parameters = parameters
        self.no_html_template = no_html_template
        self.google_tracker = google_tracker

        # Call the Gmail API
        service = gmail_authenticate()

        # The high-level workflow to send an email is to:
        # 1.1 Create the email content in some convenient way
            
        # 1.2 and encode it as a base64url string.
        

        # 2.1 Create a new message resource
        # 2.2 and set its raw property to the base64url string you just created.

        # 3. Call messages.send, or, if sending a draft, drafts.send to send the message.
        # new_email.send()



def main():
    # Email content
    receivers = ['monk3yd.thelab@gmail.com', 'example@example.com']
    subject = 'Urgente'

    # Read HTML file  # Convert to utils
    template_path = Path("templates/template.html")
    template = open_template(template_path)
    
    parameters = {
            'name': 'John Doe',
            'rut': '13.411.831-0',
        }

    # Read NO HTML file  # Convert to utils
    version_no_html_path = Path("templates/template.txt") 
    no_html_template = open_template(version_no_html_path)

    google_tracker = {}  # https://htmlemail.io/blog/google-analytics-email-tracking

    # Create email
    new_email = Email(
        receivers=receivers,  # list()
        subject=subject,  # str()
        template=template,  # str()
        parameters=parameters,  # dict()
        no_html_template=no_html_template,  # str()
        google_tracker=google_tracker  # dict()  
    )

    print(new_email)

    # except HttpError as error:
    #     # TODO(developer) - Handle errors from gmail API.
    #     print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()

# https://developers.google.com/gmail/api/quickstart/python
# https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
# https://developers.google.com/gmail/api/guides/sending