import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
    )

def add_subscriber(email,team):
    response = client.table("subscribers").insert({
        "email":email,
        "team":team
    }).execute()
    return response.data

def get_all_subscribers() :
    response = client.table("subscribers").select("*").execute()
    return response.data

def remove_subscriber(email):
    response = client.table("subscribers").delete().eq("email", email).execute()
    return response.data

def subscriber_exists(email):
    response = client.table("subscribers").select("*").eq("email", email).execute()
    return len(response.data) > 0