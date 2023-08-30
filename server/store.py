import postgrest
from supabase import Client, create_client
import os


supabase: Client = create_client(os.environ.get(
    "SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))


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
            return "invalid uuid"

        response = supabase.table('subscribers').delete().eq(
            'email_id', email_id).execute()

        return "user successfully deleted"

    except postgrest.exceptions.APIError as err:
        print(err.message)
