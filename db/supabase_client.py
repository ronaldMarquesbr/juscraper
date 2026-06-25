import os

from supabase import create_client


class SupabaseClient:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url:
            raise ValueError("SUPABASE_URL environment variable is not set")
        if not key:
            raise ValueError("SUPABASE_KEY environment variable is not set")

        self.client = create_client(url, key)
