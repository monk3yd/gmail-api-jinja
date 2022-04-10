# Project: Send Email via Gmail API (business) with Templates (jinja2) using Python
from __future__ import print_function

from pathlib import Path

# Own
from gmail import Email
from utils import open_template


def main():
    # Email content
    sender = 'monk3yd.thelab@gmail.com'
    receiver = 'monk3yd.thelab@yahoo.com'
    subject = 'Urgente'
    html_template = open_template(Path("templates/template.html"))
    parameters = {
            'name': 'John Doe',
            'age': 28,
        }
    no_html_template = open_template(Path("templates/template.txt"))
    # google_tracker = {}  # https://htmlemail.io/blog/google-analytics-email-tracking
       

    # Create email
    new_email = Email(
        sender=sender,  # list()
        receiver=receiver,  # list()
        subject=subject,  # str()
        html_template=html_template,  # str()
        parameters=parameters,  # dict()
        no_html_template=no_html_template,  # str()
        # google_tracker=google_tracker  # dict()  
    )
    # print(new_email)

    # Send email
    new_email.send()


if __name__ == '__main__':
    main()

# https://developers.google.com/gmail/api/quickstart/python
# https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
# https://developers.google.com/gmail/api/guides/sending
# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python