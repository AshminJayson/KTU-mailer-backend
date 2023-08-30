from typing import Annotated
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Form

# from uuid import uuid4

from . import store
from . import scraper
from . import mail_server

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://ktu-mailer-frontend.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def welcome(request: Request):
    return {'message': 'go to /docs to use the api'}


@app.post("/subscriber")
async def add_subscriber(email_id: str = ''):
    ret = store.add_subscriber(email_id)
    print(ret)
    return {'message': ret}


@app.delete("/subscriber")
async def delete_subscriber(email_id: str, uuid: str):
    ret = store.delete_subscriber(email_id, uuid)
    return {'message': ret}


@app.get("/push_notifications")
async def push_notifications():
    # if server_token != :

    last_notification_title = store.get_last_notification_title()
    notifications = scraper.get_notifications_upto(last_notification_title)

    if len(notifications) == 0:
        return {'message': 'No new notifications available'}

    i = 0
    while i < len(notifications):
        if notifications[i]['subject'] == last_notification_title:
            break

        # Push to clients
        i += 1

    # Push notification in reverse order
    for j in range(i-1, -1, -1):
        store.add_notification_title(notifications[j]['subject'])
        mail_server.send_mail_to_all_users(notifications[j]['body'],
                                           notifications[j]['subject'],  notifications[j]['file_data'], notifications[j]['file_name'])

    return {'new_notifications': [notification['subject'] for notification in notifications[:i]]}
