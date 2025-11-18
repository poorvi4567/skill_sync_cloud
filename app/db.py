import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def get_supabase() -> Client:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)
    return supabase
