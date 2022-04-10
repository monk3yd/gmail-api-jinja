from jinja2 import Template
from utils import gmail_authenticate, create_message, send_message

class Email():

    def __init__(self, sender, receiver, subject, parameters={}, html_template="", no_html_template="", google_tracker={}):
        # Email Object Properties
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.html_template = html_template
        self.parameters = parameters
        self.no_html_template = no_html_template
        self.google_tracker = google_tracker

        # Templating with params
        name = self.parameters['name']
        age = str(self.parameters['age'])

        tm = Template(self.html_template)
        html = tm.render(name=name, age=age)

        # Call the Gmail API
        self.service = gmail_authenticate()

        # Create message
        self.encoded_message = create_message(self.sender, self.receiver, self.subject, html, self.no_html_template) 

    # Send message
    def send(self):
        send_message(self.service, 'me', self.encoded_message) 
