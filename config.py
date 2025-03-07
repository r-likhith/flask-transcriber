# Database Config

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Load Supabase URL and Service Role Key from environment variables
DB_URL = os.getenv("DB_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Ensure both variables are present to avoid errors during initialization
if not DB_URL or not SUPABASE_API_KEY:
    raise ValueError("Missing Supabase configuration! Make sure DB_URL and SUPABASE_API_KEY are set.")

# Initialize Supabase client
supabase: Client = create_client(DB_URL, SUPABASE_API_KEY)
