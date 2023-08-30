import postgrest
from supabase import Client, create_client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_subscribers():
    try:
        response = supabase.table('subscribers').select('*').execute()
        subscribers = [[record['email_id'], record['id']]
                       for record in response.data]
        return subscribers
    except postgrest.exceptions.APIError as err:
        print(err.message)

    return []


def add_subscriber(email_id: str):
    try:
        supabase.table('subscribers').insert(
            {'email_id': email_id}).execute()
        return "user added"
    except postgrest.exceptions.APIError as err:
        if "duplicate key" in err.message:
            return "user already exists"


def delete_subscriber(email_id: str, _uuid: str):
    try:
        response = supabase.table('subscribers').select(
            "id").eq("email_id", email_id).execute()

        if response == []:
            return "user does not exist"

        if response.data[0]['id'] != _uuid:
            return "invalid user passkey"

        response = supabase.table('subscribers').delete().eq(
            'email_id', email_id).execute()

        return "user successfully deleted"

    except postgrest.exceptions.APIError as err:
        print(err.message)


def add_notification_title(notification_title: str):
    try:
        response = supabase.table('notifications').insert(
            {'notification_title': notification_title}).execute()

        return "notification title added successfully"
    except postgrest.exceptions.APIError as err:
        print(err.message)


def get_last_notification_title():
    try:
        response = supabase.table('notifications').select(
            "*").order("created_at", desc=True).limit(1).execute()

        if len(response.data) == 0:
            return ''
        return response.data[0].get('notification_title', '')
    except postgrest.exceptions.APIError as err:
        print(err.message)
