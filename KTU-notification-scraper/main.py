import re
from bs4 import BeautifulSoup
import requests
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from mail import send_mail  # nopep8

url = "https://ktu.edu.in/eu/core/announcements.htm"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
notifications = soup.find("table", {"class": "ktu-news"}).find_all("tr")


def process_notification(notification):
    print("Processing notification...")
    sections = notification.find_all("td")
    notification_metadata = sections[0]
    notification_content = sections[1].find("li")

    notification_date = notification_metadata.find("b").text

    file_download_link = "https://ktu.edu.in" + \
        notification_content.find("a")['href']

    file_request = requests.get(file_download_link)

    def get_filename(content_disposition_header):
        """Get filename from content disposition header"""
        if not content_disposition_header:
            return None

        file_name = re.findall('filename=(.+)', content_disposition_header)
        if len(file_name[0]) <= 3:
            return None

        # Remove double quotes in starting and ending
        return file_name[0][1:-1]

    file_name = get_filename(file_request.headers['Content-Disposition'])

    notification_title = notification_content.find("b").text
    notification_body = notification_content

    while notification_body.b:
        notification_body.b.decompose()

    body = notification_body.text
    subject = notification_title

    send_mail(body, subject,
              file_request.content, file_name)

    # if file_name != None:
    #     with open(file_name, 'wb') as file:
    #         file.write(file_request.content)


for i in range(3):
    process_notification(notifications[i])


# print(notification_content)
