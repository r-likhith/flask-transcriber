
# Database Config

import os
from supabase import create_client, Client

# Load Supabase URL and Service Role Key from environment variables
DB_URL = os.getenv("DB_URL", "https://vyomavsxryemnyufixw.supabase.co")  # Fallback to hardcoded URL
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5b21hdnN3eHJ5ZW1ueXVmaXh3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MTAwNDEyMCwiZXhwIjoyMDU2NTgwMTIwfQ.77CNBmiHa7Iz6TYIChgpwzaSUDyiLPOefPONcmrtOR8")

# Ensure both variables are present to avoid errors during initialization
if not DB_URL or not SUPABASE_API_KEY:
    raise ValueError("Missing Supabase configuration! Make sure DB_URL and SUPABASE_API_KEY are set.")

# Initialize Supabase client
supabase: Client = create_client(DB_URL, SUPABASE_API_KEY)
