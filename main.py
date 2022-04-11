# Project: Send Email via Gmail API (business) with Templates (jinja2) using Python
from __future__ import print_function

from pathlib import Path

# Own
from gmail import Email
from utils import open_template


def main():
    # Email content
    parameters = [
        {
            'email': 'monk3yd.thelab@yahoo.com',
            'name': 'John Doe',
            'age': 28,
        },
        {
            'email': 'monk3yd.thelab@gmail.com',
            'name': 'Walter White',
            'age': 64,
        },
    ]

    sender = 'monk3yd.thelab@gmail.com'
    receivers = [user['email'] for user in parameters] # Isn't necessary if email is included in parameters
    subject = 'Project: Send Email with Jinja Templating via Gmail API'
    html_text = open_template(Path("templates/template.html"))
    no_html_text = open_template(Path("templates/template.txt"))
    # google_tracker = {}  # https://htmlemail.io/blog/google-analytics-email-tracking
       

    # Create email
    new_email = Email(
        sender=sender,  # list()
        receivers=receivers,  # list()
        subject=subject,  # str()
        html_text=html_text,  # str()
        parameters=parameters,  # list of dicts
        no_html_text=no_html_text,  # str()
        # google_tracker=google_tracker  # dict()  
    )

    # Send email
    new_email.send()


if __name__ == '__main__':
    main()

# https://developers.google.com/gmail/api/quickstart/python
# https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
# https://developers.google.com/gmail/api/guides/sending
# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python