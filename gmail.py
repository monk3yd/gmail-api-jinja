from jinja2 import Template
from utils import gmail_authenticate, create_message, send_message

class Email():

    def __init__(self, sender, receivers, subject, parameters={}, html_text="", no_html_text="", google_tracker={}):
        # Email Object Properties
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.parameters = parameters
        self.html_text = html_text
        self.no_html_text = no_html_text
        self.google_tracker = google_tracker

        # Call the Gmail API
        self.service = gmail_authenticate()

        self.list_of_messages = []
        # Loop through all receivers creating one message for each
        for user in self.parameters:
            email = user['email']
            name = user['name']
            age = str(user['age'])

            # Templating with params variables  # TODO export to utils.py, make function template_and_render(string, params)
            html_tm = Template(self.html_text)
            html = html_tm.render(name=name, age=age)

            no_html_tm = Template(self.no_html_text)
            no_html = no_html_tm.render(name=name, age=age) 

            # Create message
            encoded_message = create_message(self.sender, email, self.subject, html, no_html) 
            self.list_of_messages.append(encoded_message)

    # Send message
    def send(self):
        for message in self.list_of_messages:
            send_message(self.service, 'me', message) 
