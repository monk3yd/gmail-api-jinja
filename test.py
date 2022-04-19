from pathlib import Path
from jinja2 import Template

from utils import open_template

def main():
    parameters = [  # Ideally imported from csv file or db. element keys represents columns, each element in list represents a row
            {
                'email': 'monk3yd.thelab@yahoo.com',
                'name': 'John Doe',
                'age': 28,
            },
            {
                'email': 'monk3yd.thelab@gmail.com',
                'name': 'Walter White',
                'age': 64,
            },
            {
                'email': 'monk3yd.thelab@protonmail.com',
                'name': 'Kvothe Kingkiller',
                'age': 37,
            }
        ]
    html_text = open_template(Path("templates/template.html"))

    for user in parameters:
        # Templating HTML with params and pixelURL variables
        # TODO - Automatically prepopulate .render() function *kwargs with user key/value pairs
        html_tm = Template(html_text)
        html = html_tm.render(**user, pixelURL_tracker="akhjdfkjaskdjfhjdaks")
        # html = html_tm.render(
        #     name=name,
        #     age=age,
        #     pixelURL_tracker=pixelURL_tracker
        # )

        print(html)

def create_pixelURL_tracker(google_tracker):
    tracking_id = google_tracker['tracking_id']
    client_id = int(google_tracker['client_id'])
    anonymize_ip = int(google_tracker['anonymize_ip'])
    tracker_path = urllib.parse.quote(google_tracker['tracker_path'], safe='')
    tracker_title = urllib.parse.quote(google_tracker['tracker_title'], safe='')
    return f'https://www.google-analytics.com/collect?v=1&tid={tracking_id}&cid={client_id}&aip={anonymize_ip}&t=event&ec=email&ea=open&dp={tracker_path}&dt={tracker_title}'

main()