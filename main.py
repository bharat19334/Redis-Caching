import time
import json
from fastapi import FastAPI, HTTPException, Query
from config import supabase, redis_client, CACHE_KEY, CACHE_TTL
from models import ProductCreate

app = FastAPI(title="Redis Caching Lab Task")

@app.get("/products")
def get_products(use_cache: bool = Query(True)):
    start_time = time.perf_counter()

    # 1. Check Redis Cache[cite: 1]
    if use_cache:
        cached_data = redis_client.get(CACHE_KEY)
        if cached_data:
            latency = round((time.perf_counter() - start_time) * 1000, 2)
            print(f"[LOG] Served from: REDIS CACHE | Time: {latency} ms")
            return {
                "source": "Redis Cache",
                "latency_ms": latency,
                "ttl_remaining_seconds": redis_client.ttl(CACHE_KEY),
                "count": len(json.loads(cached_data)),
                "data": json.loads(cached_data)
            }

    # 2. Query Supabase (Primary DB) on Cache Miss[cite: 1]
    response = supabase.table("products").select("*").order("id").execute()
    products = response.data

    # 3. Save in Redis with 60s TTL[cite: 1]
    if use_cache and products:
        redis_client.setex(CACHE_KEY, CACHE_TTL, json.dumps(products))

    latency = round((time.perf_counter() - start_time) * 1000, 2)
    print(f"[LOG] Served from: SUPABASE (Primary DB) | Time: {latency} ms")

    return {
        "source": "Primary Data Source (Supabase)",
        "latency_ms": latency,
        "ttl_remaining_seconds": CACHE_TTL if use_cache else None,
        "count": len(products),
        "data": products
    }

@app.post("/products")
def add_product(product: ProductCreate):
    start_time = time.perf_counter()

    # 1. Insert new product into Supabase[cite: 1]
    response = supabase.table("products").insert(product.model_dump()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to add product")

    # 2. Invalidate Redis Cache[cite: 1]
    is_deleted = redis_client.delete(CACHE_KEY)
    latency = round((time.perf_counter() - start_time) * 1000, 2)
    
    print(f"[LOG] Product added. Cache Invalidated: {bool(is_deleted)}")

    return {
        "message": "Product added and cache invalidated",
        "cache_invalidated": bool(is_deleted),
        "latency_ms": latency,
        "product": response.data[0]
    }