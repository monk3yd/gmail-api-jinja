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

        # Call the Gmail API
        self.service = gmail_authenticate()

        # Create message
        self.encoded_message = create_message(self.sender, self.receiver, self.subject, self.html_template, self.no_html_template) 

    # Send message
    def send(self):
        send_message(self.service, 'me', self.encoded_message) 
                

# The high-level workflow to send an email is to:
    # 1.1 Create the email content

    # 1.2 and encode it as a base64url string.

    # 2.1 Create a new message resource

    # 2.2 and set its raw property to the base64url string you just created.

    # 3. Call messages.send, or, if sending a draft, drafts.send to send the message.
 