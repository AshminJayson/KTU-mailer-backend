import re
from bs4 import BeautifulSoup
import requests


def get_notifications():
    url = "https://ktu.edu.in/eu/core/announcements.htm"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    notifications = soup.find("table", {"class": "ktu-news"}).find_all("tr")
    res = []
    for i in range(len(notifications)):
        res.append(process_notification(notifications[i]))

    return res


def get_filename(content_disposition_header):
    """Get filename from content disposition header"""
    if not content_disposition_header:
        return None

    file_name = re.findall('filename=(.+)', content_disposition_header)
    if len(file_name[0]) <= 3:
        return None

    # Remove double quotes in starting and ending
    return file_name[0][1:-1]


def process_notification(notification):
    sections = notification.find_all("td")
    notification_metadata = sections[0]
    notification_content = sections[1].find("li")

    # notification_date = notification_metadata.find("b").text

    # Get notification attachment if present
    file_download_link = "https://ktu.edu.in" + \
        notification_content.find("a")['href']
    file_request = requests.get(file_download_link)
    file_name = get_filename(file_request.headers['Content-Disposition'])

    # Notification title is the first <b> in the body
    notification_title = notification_content.find("b").text
    notification_body = notification_content

    # Remove all <b> tags from body that have no relevant information
    while notification_body.b:
        notification_body.b.decompose()

    body = notification_body.text
    subject = notification_title

    print(f"Processing notification : [{notification_title}]")

    return [subject, body, file_request.content, file_name]

    # To hold local copy of notification_file
    # if file_name != None:
    #     with open(file_name, 'wb') as file:
    #         file.write(file_request.content)


# print(notification_content)
