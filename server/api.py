from typing import Annotated
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Form

# from uuid import uuid4

from . import store
from . import scraper

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
async def welcome(request: Request):
    return {'message': 'go to /docs to use the api'}


@app.post("/subscriber/")
async def add_subscriber(email_id: str = ''):
    ret = store.add_subscriber(email_id)
    print(ret)
    return {'message': ret}


@app.delete("/subscriber")
async def delete_subscriber(email_id: str, uuid: str):
    ret = store.delete_subscriber(email_id, uuid)
    return {'message': ret}


@app.get("/push_notifications")
async def push_notifications(server_token):
    # if server_token != :

    notifications = scraper.get_notifications()
    print(notifications)

    return {'message': [notification[0] for notification in notifications]}
