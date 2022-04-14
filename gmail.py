import urllib.parse
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

        tracking_id = google_tracker['tracking_id']
        client_id = int(google_tracker['client_id'])
        anonymize_ip = int(google_tracker['anonymize_ip'])

        tracker_path = urllib.parse.quote(google_tracker['tracker_path'], safe='')
        tracker_title = urllib.parse.quote(google_tracker['tracker_title'], safe='')

        # tracker_path = google_tracker['tracker_path'].replace('/', '%2')
        # tracker_title = google_tracker['tracker_title'].replace(' ', '%20')

        # Loop through all receivers creating one message for each
        for user in self.parameters:
            email = user['email']
            name = user['name']
            age = str(user['age'])
            
            # Templating with params variables  # TODO export to utils.py, make function template_and_render(string, params)
            html_tm = Template(self.html_text)
            html = html_tm.render(
                name=name,
                age=age,
                tracking_id=tracking_id,
                client_id=client_id,
                anonymize_ip=anonymize_ip,
                tracker_path=tracker_path,
                tracker_title=tracker_title
            )  # kwargs**  ?? TODO render automatically

            no_html_tm = Template(self.no_html_text)
            no_html = no_html_tm.render(name=name, age=age, tracking_id=google_tracker['tracking_id'])  # A real no_html email can't be tracked. Need hybrid email. 

            # Create message
            encoded_message = create_message(self.sender, email, self.subject, html, no_html) 
            self.list_of_messages.append(encoded_message)

    # Send message
    def send(self):
        for message in self.list_of_messages:
            send_message(self.service, 'me', message) 
