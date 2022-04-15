from utils import gmail_authenticate, send_message, create_pixelURL_tracker, create_all_messages


class Email():

    def __init__(self, sender, receivers, subject, parameters={}, html_text="", no_html_text="", attachment="", google_tracker={}):
        # Email Object Properties
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.parameters = parameters
        self.html_text = html_text
        self.no_html_text = no_html_text

        # Call the Gmail API
        self.service = gmail_authenticate()

        # Setup trackable pixelURL
        self.pixelURL_tracker = create_pixelURL_tracker(google_tracker)

        # Stores all encoded messages
        self.all_encoded_messages = create_all_messages(
                sender=self.sender,
                subject=self.subject,
                parameters=self.parameters,
                pixelURL_tracker=self.pixelURL_tracker,
                html_text=self.html_text,
                no_html_text=self.no_html_text,
                attachment=attachment
            )

    # Send messages
    def send(self):
        for message in self.all_encoded_messages:
            send_message(self.service, 'me', message) 
