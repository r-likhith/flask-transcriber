# Database Config

import os
from supabase import create_client

# Load Supabase URL and Service Role Key from environment variables
DB_URL = os.getenv("DB_URL", "https://vyomavswxryemnyufixw.supabase.co")  # Fallback to hardcoded if not provided
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5b21hdnN3eHJ5ZW1ueXVmaXh3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MTAwNDEyMCwiZXhwIjoyMDU2NTgwMTIwfQ.77CNBmiHa7Iz6TYIChgpwzaSUDyiLPOefPONcmrtOR8")  # Truncated example key

# Initialize Supabase client
supabase = create_client(DB_URL, SUPABASE_API_KEY)
