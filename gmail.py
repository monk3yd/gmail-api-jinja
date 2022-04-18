from utils import gmail_authenticate, send_message, create_pixelURL_tracker, create_all_messages


class Email():

    def __init__(self, sender: str, receivers: list, subject: str, parameters: list, html_text: str, no_html_text: str = None, google_tracker: dict = None, attachments: list = None) -> None:
        # Email Object Properties
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.parameters = parameters
        self.html_text = html_text
        self.no_html_text = no_html_text
        self.pixelURL_tracker = google_tracker
        self.attachments = attachments

        # Call the Gmail API
        self.service = gmail_authenticate()

        if google_tracker is not None:
            # Setup trackable pixelURL
            self.pixelURL_tracker = create_pixelURL_tracker(google_tracker)

        # Stores all encoded messages
        self.all_encoded_messages = create_all_messages(
                sender=self.sender,
                subject=self.subject,
                parameters=self.parameters,
                html_text=self.html_text,
                no_html_text=self.no_html_text,
                pixelURL_tracker=self.pixelURL_tracker,
                attachments=self.attachments
            )

    # Send messages
    def send(self):
        for message in self.all_encoded_messages:
            send_message(self.service, 'me', message)
