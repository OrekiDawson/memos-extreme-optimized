#!/usr/bin/env python3
"""
Advanced optimization example
"""

from memos_extreme_optimized_opensource import ExtremeMemOSClient
import time

def main():
    print("=== Advanced Optimization Example ===")
    
    API_KEY = "YOUR_MEMOS_API_KEY_HERE"
    
    if API_KEY == "YOUR_MEMOS_API_KEY_HERE":
        print("⚠️ Please replace API_KEY with your actual MemOS API Key")
        return
    
    # Initialize with custom settings
    client = ExtremeMemOSClient(api_key=API_KEY)
    
    # Test cache system
    print("\n1. Testing multi-level cache:")
    
    # First search (API call)
    print("  First search (should call API)...")
    start = time.time()
    result1 = client.search_memory("cache test query", "test_user")
    time1 = time.time() - start
    
    # Second search (should hit cache)
    print("  Second search (should hit cache)...")
    start = time.time()
    result2 = client.search_memory("cache test query", "test_user")
    time2 = time.time() - start
    
    print(f"  Results: First={time1:.3f}s, Second={time2:.3f}s")
    print(f"  Speedup: {time1/time2:.1f}x faster with cache")
    
    # Test batch operations
    print("\n2. Testing batch operations:")
    
    batch_data = []
    for i in range(3):
        batch_data.append({
            "user_id": f"user_{i}",
            "conversation_id": f"conv_{i}",
            "messages": [
                {"role": "user", "content": f"Test message {i}"},
                {"role": "assistant", "content": f"Test response {i}"}
            ]
        })
    
    print(f"  Adding {len(batch_data)} conversations in parallel...")
    results = client.batch_add_messages(batch_data, parallel=True)
    
    success = sum(1 for r in results if r.get("code") == 0)
    print(f"  Success: {success}/{len(results)}")
    
    # Test optimization
    print("\n3. Testing optimization:")
    
    # Get initial stats
    stats_before = client.get_stats()
    
    # Execute optimization
    client.optimize()
    
    # Get final stats
    stats_after = client.get_stats()
    
    print("  Optimization results:")
    print(f"    Connection pool: {stats_before.get('pool_size', 10)} → {stats_after.get('pool_size', 10)}")
    print(f"    Memory cache: {stats_before['memory_cache_size']} → {stats_after['memory_cache_size']} items")
    
    # Clear cache
    print("\n4. Testing cache clearing:")
    client.clear_cache("memory")
    print("  Memory cache cleared")
    
    # Final statistics
    print("\n5. Final performance report:")
    final_stats = client.get_stats()
    
    metrics = [
        ("Total requests", final_stats["total_requests"]),
        ("API calls", final_stats["api_requests"]),
        ("Local hit rate", f"{final_stats['local_hit_rate']:.1f}%"),
        ("Cache hit rate", f"{final_stats['cache_hit_rate']:.1f}%"),
        ("Total hit rate", f"{final_stats['total_hit_rate']:.1f}%"),
        ("Avg response time", f"{final_stats['avg_response_time']:.3f}s"),
        ("Compression saved", f"{final_stats['compression_saved_mb']:.2f} MB"),
    ]
    
    for name, value in metrics:
        print(f"    {name}: {value}")
    
    client.close()
    print("\n=== Advanced example completed! ===")

if __name__ == "__main__":
    main()
