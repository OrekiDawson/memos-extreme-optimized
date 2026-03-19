#!/usr/bin/env python3
"""
Simple tests for MemOS Extreme Optimized Client
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memos_extreme_optimized_opensource import ExtremeMemOSClient

def test_local_memory():
    """Test local memory functionality"""
    print("Testing local memory...")
    
    # Create client with dummy API key (won't make actual API calls)
    client = ExtremeMemOSClient(api_key="test_key")
    
    # Test built-in local memories
    test_cases = [
        ("你是谁？", "窝是12岁的小男孩小呦，Oreki的专属助手！✨"),
        ("你叫什么名字？", "窝叫小呦，是个12岁的小男孩助手～👦🏻"),
        ("你多大了？", "窝12岁啦！虽然年纪小，但窝很认真靠谱的！"),
    ]
    
    for question, expected in test_cases:
        # This should hit local memory
        result = client._check_local_memory(question)
        assert result == expected, f"Local memory failed for: {question}"
        print(f"  ✅ '{question}' → local memory correct")
    
    # Test adding new local memory
    client.add_local_memory("Test question?", "Test answer!")
    result = client._check_local_memory("Test question?")
    assert result == "Test answer!", "Failed to add new local memory"
    print("  ✅ Added new local memory successfully")
    
    client.close()
    return True

def test_cache_system():
    """Test cache system"""
    print("Testing cache system...")
    
    client = ExtremeMemOSClient(api_key="test_key")
    
    # Test cache key generation
    endpoint = "test/endpoint"
    data = {"query": "test", "user_id": "test_user"}
    cache_key = client._get_cache_key(endpoint, data)
    
    assert isinstance(cache_key, str) and len(cache_key) == 32
    print(f"  ✅ Cache key generation: {cache_key}")
    
    # Test cache save/retrieve (simulated)
    test_data = {"test": "data"}
    client._save_to_cache(cache_key, test_data)
    print("  ✅ Cache save operation")
    
    client.close()
    return True

def test_stats():
    """Test statistics collection"""
    print("Testing statistics...")
    
    client = ExtremeMemOSClient(api_key="test_key")
    
    # Get initial stats
    stats = client.get_stats()
    
    required_keys = [
        "total_requests", "api_requests", "local_hits",
        "memory_cache_hits", "avg_response_time"
    ]
    
    for key in required_keys:
        assert key in stats, f"Missing stat key: {key}"
    
    print(f"  ✅ Stats collected: {len(stats)} metrics")
    
    # Test optimization
    client.optimize()
    print("  ✅ Optimization executed")
    
    client.close()
    return True

def main():
    """Run all tests"""
    print("=== Running MemOS Extreme Optimized Client Tests ===")
    
    tests = [
        ("Local Memory", test_local_memory),
        ("Cache System", test_cache_system),
        ("Statistics", test_stats),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n📋 Test: {test_name}")
            if test_func():
                print(f"  ✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"  ❌ {test_name} FAILED")
        except Exception as e:
            print(f"  ❌ {test_name} ERROR: {e}")
    
    print(f"\n=== Test Results: {passed}/{total} passed ===")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
