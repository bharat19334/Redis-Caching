import os
from dotenv import load_dotenv
from supabase import create_client, Client
import fakeredis

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 1. Supabase Primary DB Connection
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. In-Memory Redis Server (Bina external software install kiye chalega)
redis_client = fakeredis.FakeStrictRedis(decode_responses=True)

CACHE_KEY = "products_list"
CACHE_TTL = 60  # 60 seconds expiration time