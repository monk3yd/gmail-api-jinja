# Project: Send Email via Gmail API (business) with HTML Templates (jinja2) using Python

from __future__ import print_function  # ??

from pathlib import Path

# Own classes and functions
from gmail import Email
from utils import open_template


def main():
    # Email content
    parameters = [  # Ideally imported from csv file or db. element keys represents columns, each element in list represents a row
        {
            'email': 'monk3yd.thelab@yahoo.com',
            'name': 'John Doe',
            'age': 28,
        },
        # {
        #     'email': 'monk3yd.thelab@gmail.com',
        #     'name': 'Walter White',
        #     'age': 64,
        # },
        # {
        #     'email': 'monk3yd.thelab@protonmail.com',
        #     'name': 'Kvothe Kingkiller',
        #     'age': 37,
        # }
    ]

    sender = 'monk3yd.thelab@gmail.com'
    receivers = [user['email'] for user in parameters]  # Isn't necessary if email is included in parameters
    subject = 'Project: Send Email via Gmail API with HTML Templates (jinja2) using Python'
    html_text = open_template(Path("templates/template.html"))

    # Optional email content 
    no_html_text = open_template(Path("templates/template.txt"))
    attachment_file = Path("attachments/test.txt")
    google_tracker = {
        'tracking_id': 'UA-226021269-1',
        'client_id': 555,  # anonymous  # Hardcode?
        'anonymize_ip': 1,  # 1=enable  # Hardcode?
        'tracker_path': '/email/tracker',  # Hardcode?
        'tracker_title': 'My Email Tracker'  # Hardcode?
    }  

    # Create email
    new_email = Email(
        sender=sender,  # str(), ideally list()
        receivers=receivers,  # list()
        subject=subject,  # str()
        parameters=parameters,  # list of dicts
        html_text=html_text,  # str()
        no_html_text=no_html_text,  # str()
        google_tracker=google_tracker,  # dict()
        attachment=attachment_file,  # list()
    )

    # Send email
    new_email.send()


if __name__ == '__main__':
    main()

# https://developers.google.com/gmail/api/quickstart/python
# https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
# https://developers.google.com/gmail/api/guides/sending
# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python
# https://zetcode.com/python/jinja/
# https://htmlemail.io/blog/google-analytics-email-tracking
# https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-with-attachments-in-python/