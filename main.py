from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from uuid import uuid4

import store
import scraper
import mail_server

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def welcome():
    return {'message': 'Go to /docs to test the api'}


@app.get("/add_subscriber")
async def add_subscriber(email_id: str):
    ret = store.add_subscriber(email_id)
    return {'message': ret}


@app.get("/delete_subscriber")
async def delete_subscriber(email_id: str, uuid: str):
    ret = store.delete_subscriber(email_id, uuid)
    return {'message': ret}


@app.get("/push_notifications")
async def push_notifications(server_token):
    # if server_token != :

    notifications = scraper.get_notifications()
    print(notifications)

    return {'message': [notification[0] for notification in notifications]}
