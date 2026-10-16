import requests

BASE_URL = "http://127.0.0.1:8000"

print("\n==================================================")
print("🚀 RUNNING REDIS CACHING BENCHMARK TEST")
print("==================================================\n")

try:
    print("1: First Request (Without Redis / Supabase Cache Miss) ---")
    r1 = requests.get(f"{BASE_URL}/products").json()
    print(f"Source: {r1.get('source')} | Time: {r1.get('latency_ms')} ms | Products: {r1.get('count')}\n")

    print("2: Second Request (With Redis / Cache Hit) ---")
    r2 = requests.get(f"{BASE_URL}/products").json()
    print(f"Source: {r2.get('source')} | Time: {r2.get('latency_ms')} ms | TTL Left: {r2.get('ttl_remaining_seconds')}s\n")

    print("3: Adding New Product (Cache Invalidation) ---")
    new_prod = {"name": "Smart Watch", "price": 2999, "category": "Wearables", "stock": 15}
    r_post = requests.post(f"{BASE_URL}/products", json=new_prod).json()
    print(f"Status: {r_post.get('message')} | Cache Deleted: {r_post.get('cache_invalidated')}\n")

    print("4: Request After Adding Product (Fresh from Supabase) ---")
    r3 = requests.get(f"{BASE_URL}/products").json()
    print(f"Source: {r3.get('source')} | Time: {r3.get('latency_ms')} ms\n")

    print("5: Next Request (Back to Redis Cache Hit) ---")
    r4 = requests.get(f"{BASE_URL}/products").json()
    print(f"Source: {r4.get('source')} | Time: {r4.get('latency_ms')} ms\n")

    speedup = round(r1.get('latency_ms', 1) / max(r2.get('latency_ms', 1), 0.05), 1)
    print(f"=== RESULT: Redis Cache was ~{speedup}x FASTER than Supabase! ===")

except requests.exceptions.ConnectionError:
    print("\n❌ [ERROR] Could not connect to the server!")
    print("👉 First run this command in your first terminal: uvicorn main:app --reload\n")

except Exception as e:
    print(f"\n❌ [ERROR] An unexpected error occurred: {e}\n")

input("\nPress Enter to close... (Test Finished)")