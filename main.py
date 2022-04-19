# Project: Send Email via Gmail API with HTML Templates (jinja2) using Python

import pandas as pd
from pathlib import Path

# My libraries
from gmail import Email
from utils import open_template, load_attachments


def main():
    # Load parameters data in csv file into pandas dataframe
    df = pd.read_csv(Path("data.csv"))  # TODO replace NaN values from columns to empty strings

    # Email contents
    parameters = df.to_dict(orient="records")  # Convert dataframe to list of dicts, element keys represent the variables names that can be used in the HTML jinja template 
    sender = "monk3yd.thelab@gmail.com"
    receivers = [user["email"] for user in parameters]  # Isn't necessary if email is included in parameters
    subject = "Project: Send Email via Gmail API with HTML Templates (jinja2) using Python"
    html_text = open_template(Path("templates/template.html"))

    # Optional email contents
    no_html_text = open_template(Path("templates/template.txt"))
    attachments = load_attachments(Path("attachments"))

    # TODO - If hardcode make function setup_gtracker() input tracking_id outputs google_tracker
    google_tracker = {
        "tracking_id": "UA-226021269-1",
        "client_id": 555,  # anonymous  # Hardcode?
        "anonymize_ip": 1,  # 1=enable  # Hardcode?
        "tracker_path": "/email/tracker",  # Hardcode?
        "tracker_title": "My Email Tracker"  # Hardcode?
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
        attachments=attachments,  # list()
    )

    # Send email
    new_email.send()


if __name__ == "__main__":
    main()
