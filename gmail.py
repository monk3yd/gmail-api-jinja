from jinja2 import Template
from utils import gmail_authenticate, create_message, send_message, create_pixelURL_tracker

class Email():

    def __init__(self, sender, receivers, subject, parameters={}, html_text="", no_html_text="", google_tracker={}):
        # Email Object Properties
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.parameters = parameters
        self.html_text = html_text
        self.no_html_text = no_html_text
        # self.google_tracker = google_tracker

        # Stores all encoded messages
        self.list_of_messages = []

        # Call the Gmail API
        self.service = gmail_authenticate()

        # Setup trackable pixelURL
        pixelURL_tracker = create_pixelURL_tracker(google_tracker)

        # Loop through all receivers creating one message for each
        for user in self.parameters:
            email = user['email']
            name = user['name']
            age = str(user['age'])
            
            # TODO export to utils.py, make function template_and_render(string, params)
            # Templating HTML with params and pixelURL variables  
            html_tm = Template(self.html_text)
            html = html_tm.render(
                name=name,
                age=age,
                pixelURL_tracker=pixelURL_tracker
            )  # kwargs**  ?? TODO render automatically

            no_html_tm = Template(self.no_html_text)
            no_html = no_html_tm.render(name=name, age=age)  # A real no_html email can't be tracked. Need hybrid email. 

            # Create message
            encoded_message = create_message(self.sender, email, self.subject, html, no_html) 
            self.list_of_messages.append(encoded_message)

    # Send message
    def send(self):
        for message in self.list_of_messages:
            send_message(self.service, 'me', message) 
