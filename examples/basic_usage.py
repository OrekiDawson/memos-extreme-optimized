#!/usr/bin/env python3
"""
Basic usage example for MemOS Extreme Optimized Client
"""

from memos_extreme_optimized_opensource import ExtremeMemOSClient

def main():
    print("=== MemOS Extreme Optimized Client - Basic Usage ===")
    
    # Replace with your actual API Key
    API_KEY = "YOUR_MEMOS_API_KEY_HERE"
    
    if API_KEY == "YOUR_MEMOS_API_KEY_HERE":
        print("⚠️ Please replace API_KEY with your actual MemOS API Key")
        print("Get your API Key from: https://memos-dashboard.openmem.net/")
        return
    
    # Initialize client
    print("1. Initializing extremely optimized client...")
    client = ExtremeMemOSClient(api_key=API_KEY)
    
    # Test local memory (0-second response)
    print("\n2. Testing local memory optimization:")
    test_queries = [
        "你是谁？",
        "你叫什么名字？",
        "你多大了？",
        "谢谢",
        "你好"
    ]
    
    for query in test_queries:
        result = client.search_memory(query, "test_user")
        if result.get("code") == 0:
            cache_type = result["data"].get("cache_type", "unknown")
            print(f"  ✅ '{query}' → {cache_type} cache")
    
    # View optimization statistics
    print("\n3. Optimization statistics:")
    stats = client.get_stats()
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Local hit rate: {stats['local_hit_rate']:.1f}%")
    print(f"  Total hit rate: {stats['total_hit_rate']:.1f}%")
    print(f"  Avg response time: {stats['avg_response_time']:.3f}s")
    
    # Add local memory
    print("\n4. Adding custom local memory:")
    client.add_local_memory(
        "What is extreme optimization?",
        "Extreme optimization means achieving 100% local hit rate and 0-second response time!"
    )
    
    # Execute optimization
    print("\n5. Executing optimization...")
    client.optimize()
    
    # Close client
    client.close()
    
    print("\n=== Example completed successfully! ===")

if __name__ == "__main__":
    main()
