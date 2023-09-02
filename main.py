import uvicorn
import os

os.environ['SUPABASE_URL'] = "https://vhesqmfeyexpjckfuavo.supabase.co"
os.environ['SUPABASE_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoZXNxbWZleWV4cGpja2Z1YXZvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MzMzNTQyNSwiZXhwIjoyMDA4OTExNDI1fQ.yGPmmmEQid6iSaHcfOZxiI8JuqBP0X33jcsOnb8Gt0w"
os.environ['SENDER_MAIL_ID'] = "kronosdestroyer54@gmail.com"
os.environ['SENDER_PASSKEY'] = "schfnluzmtiyvlhy"
os.environ['SERVER_TOKEN'] = 'd799201f-75c6-4202-b02b-89b34e0fbf28'


if __name__ == "__main__":
    uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)
