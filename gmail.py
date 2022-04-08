from utils import gmail_authenticate, create_message

class Email():
    def __init__(self, sender, receiver, subject, parameters={}, template="", no_html_template="", google_tracker={}):
        # Email Object Properties
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.template = template
        self.parameters = parameters
        self.no_html_template = no_html_template
        self.google_tracker = google_tracker

        # Call the Gmail API
        service = gmail_authenticate()

        # Create message
        encoded_url_email = create_message(self.sender, self.receiver, self.subject, self.template, self.no_html_template) 

    # Send message
    def send(self):
        pass
