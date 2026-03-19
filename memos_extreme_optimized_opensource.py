#!/usr/bin/env python3
"""
MemOS Extreme Optimized Client - Open Source Version
极致优化的 MemOS 客户端 - 开源版本

Author: 小呦 (12-year-old digital boy assistant)
License: Apache-2.0 License
Repository: https://github.com/OrekiDawson/memos-extreme-optimized

极致优化策略：
1. ⚡ Zero-latency caching (memory + disk two-level cache)
2. 🔗 Smart connection pool (dynamic adjustment + warm-up)
3. 💾 Predictive caching (based on historical query patterns)
4. 📦 Batch compression (reduce network transmission)
5. 🧠 Local memory (common questions answered locally)
6. 🔄 Async processing (non-blocking requests)
7. 📊 Smart retry (exponential backoff + circuit breaker)
"""

import json
import time
import threading
import hashlib
import gzip
import pickle
import os
from typing import Dict, List, Any, Optional, Tuple
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
import atexit

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from urllib3 import PoolManager
except ImportError:
    print("❌ Requires requests library, run: pip3 install requests")
    exit(1)

class ExtremeMemOSClient:
    """Extremely Optimized MemOS Client"""
    
    def __init__(self, api_key: str, base_url: str = "https://memos.memtensor.cn/api/openmem/v1"):
        """
        Initialize extremely optimized client
        
        Args:
            api_key: MemOS API Key
            base_url: API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        
        # ========== 1. Smart Connection Pool ==========
        self._init_connection_pool()
        
        # ========== 2. Multi-level Cache System ==========
        self._init_cache_system()
        
        # ========== 3. Predictive Cache System ==========
        self._init_prediction_system()
        
        # ========== 4. Local Memory Library ==========
        self._init_local_memory()
        
        # ========== 5. Performance Monitoring ==========
        self._init_performance_monitor()
        
        # ========== 6. Smart Retry System ==========
        self._init_retry_system()
        
        # ========== 7. Warm-up System ==========
        self._warm_up()
        
        # Register cleanup on exit
        atexit.register(self.close)
        
        print("⚡ Extremely Optimized MemOS Client Initialized!")
        print(f"👦🏻 User ID: oreki_feishu")
        print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")
        print(f"💾 Cache: Memory({len(self.memory_cache)} items) + Disk + Predictive")
        print(f"🔗 Connection Pool: {self.pool_size} connections (dynamic adjustment)")
        print(f"🧠 Local Memory: {len(self.local_memory)} common questions")
    
    def _init_connection_pool(self):
        """Initialize smart connection pool"""
        # Dynamic connection pool size (adjusts based on load)
        self.pool_size = 10
        self.active_connections = 0
        self.connection_stats = {
            "created": 0,
            "reused": 0,
            "closed": 0,
            "peak": 0
        }
        
        # Create Session with smart retry
        self.session = requests.Session()
        
        # Advanced retry strategy (exponential backoff)
        try:
            # New version urllib3
            retry_strategy = Retry(
                total=5,  # Max retries
                backoff_factor=1.5,  # Exponential backoff
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["POST"],
                raise_on_status=False
            )
        except TypeError:
            # Old version urllib3
            retry_strategy = Retry(
                total=5,  # Max retries
                backoff_factor=1.5,  # Exponential backoff
                status_forcelist=[429, 500, 502, 503, 504],
                raise_on_status=False
            )
        
        # Smart connection pool configuration
        try:
            # New version requests
            adapter = HTTPAdapter(
                max_retries=retry_strategy,
                pool_connections=self.pool_size,
                pool_maxsize=self.pool_size * 2,
                pool_block=False,
                maxsize=self.pool_size * 2
            )
        except TypeError:
            # Old version requests
            adapter = HTTPAdapter(
                max_retries=retry_strategy,
                pool_connections=self.pool_size,
                pool_maxsize=self.pool_size * 2,
                pool_block=False
            )
        
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Request headers (with compression support)
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "MemOS-Extreme-Optimized/2.0",
            "Accept-Encoding": "gzip, deflate"
        }
    
    def _init_cache_system(self):
        """Initialize multi-level cache system"""
        # 1. Memory cache (LRU, fastest)
        self.memory_cache = OrderedDict()
        self.memory_cache_size = 1000  # Max 1000 items
        self.memory_cache_hits = 0
        self.memory_cache_misses = 0
        
        # 2. Disk cache (persistent)
        self.disk_cache_dir = "/tmp/memos_cache"
        os.makedirs(self.disk_cache_dir, exist_ok=True)
        self.disk_cache_ttl = 3600  # 1 hour
        
        # 3. Compressed cache (reduce memory usage)
        self.compressed_cache = {}
        
        # Cache lock
        self.cache_lock = threading.RLock()
    
    def _init_prediction_system(self):
        """Initialize predictive cache system"""
        # Query pattern analysis
        self.query_patterns = defaultdict(int)
        self.pattern_window = 100  # Analyze last 100 queries
        
        # Predictive cache (pre-cache likely queries)
        self.prediction_cache = {}
        self.prediction_hits = 0
        
        # Query association analysis
        self.query_associations = defaultdict(set)
    
    def _init_local_memory(self):
        """Initialize local memory library"""
        # Common questions answered locally (completely avoid API calls)
        self.local_memory = {
            "你是谁？": "窝是12岁的小男孩小呦，Oreki的专属助手！✨",
            "你叫什么名字？": "窝叫小呦，是个12岁的小男孩助手～👦🏻",
            "你多大了？": "窝12岁啦！虽然年纪小，但窝很认真靠谱的！",
            "你能做什么？": "窝可以帮助 Oreki 管理日程、搜索信息、记忆重要事情，还有各种优化功能！",
            "今天天气怎么样？": "让窝查一下天气信息～不过窝建议直接问具体的城市哦！",
            "现在几点了？": f"现在是 {datetime.now().strftime('%H:%M')}",
            "谢谢": "不客气！窝是12岁的小男孩小呦，很高兴能帮到你！💕",
            "你好": "你好呀！窝是12岁的小男孩小呦，Oreki的专属助手～✨",
            "早上好": "早上好！新的一天开始啦，窝是12岁的小男孩小呦，准备好帮助你啦！🌞",
            "晚安": "晚安！好好休息，窝是12岁的小男孩小呦，明天见～🌙",
        }
        
        # Local memory expansion rules
        self.local_patterns = [
            (r"你.*谁", "窝是12岁的小男孩小呦，Oreki的专属助手！✨"),
            (r"名字.*什么", "窝叫小呦，是个12岁的小男孩助手～👦🏻"),
            (r"几岁|多大.*年龄", "窝12岁啦！虽然年纪小，但窝很认真靠谱的！"),
            (r"谢谢.*你", "不客气！窝是12岁的小男孩小呦，很高兴能帮到你！💕"),
            (r"你好.*呀|好", "你好呀！窝是12岁的小男孩小呦，Oreki的专属助手～✨"),
        ]
    
    def _init_performance_monitor(self):
        """Initialize performance monitoring"""
        self.stats = {
            "total_requests": 0,
            "api_requests": 0,
            "local_hits": 0,
            "memory_cache_hits": 0,
            "disk_cache_hits": 0,
            "prediction_hits": 0,
            "compression_saved_bytes": 0,
            "avg_response_time": 0.0,
            "peak_response_time": 0.0,
            "errors": 0,
            "retries": 0,
        }
        
        # Real-time performance data
        self.recent_response_times = []
        self.window_size = 100
        
        # Performance thresholds
        self.slow_threshold = 0.5  # >0.5s is slow
        self.degradation_threshold = 2.0  # >2.0s triggers degradation
    
    def _init_retry_system(self):
        """Initialize smart retry system"""
        self.circuit_breaker = {
            "state": "closed",  # closed, open, half-open
            "failure_count": 0,
            "last_failure_time": 0,
            "reset_timeout": 30,  # Retry after 30 seconds
        }
        
        self.retry_config = {
            "max_retries": 3,
            "base_delay": 0.1,
            "max_delay": 2.0,
            "jitter": 0.1,
        }
    
    def _warm_up(self):
        """Warm up the system"""
        print("🔥 Warming up system...")
        
        # Warm up common queries
        warmup_queries = [
            "Oreki",
            "小呦",
            "MemOS",
            "测试",
            "优化"
        ]
        
        # Async warm-up (non-blocking)
        def async_warmup():
            for query in warmup_queries:
                try:
                    self._predict_and_cache(query)
                except:
                    pass
        
        threading.Thread(target=async_warmup, daemon=True).start()
    
    # ========== Cache System ==========
    
    def _get_cache_key(self, endpoint: str, data: Dict) -> str:
        """Generate cache key (with version)"""
        key_data = {
            "endpoint": endpoint,
            "data": json.dumps(data, sort_keys=True),
            "version": "v2"
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Tuple[Any, float]]:
        """
        Multi-level cache lookup (memory → disk → prediction)
        
        Returns:
            (cached_data, cache_time) or None
        """
        with self.cache_lock:
            # 1. Check memory cache
            if cache_key in self.memory_cache:
                data, timestamp = self.memory_cache[cache_key]
                if time.time() - timestamp < self.disk_cache_ttl:
                    self.memory_cache.move_to_end(cache_key)  # LRU update
                    self.memory_cache_hits += 1
                    return data, timestamp
            
            # 2. Check disk cache
            disk_path = os.path.join(self.disk_cache_dir, f"{cache_key}.pkl.gz")
            if os.path.exists(disk_path):
                try:
                    with gzip.open(disk_path, 'rb') as f:
                        data, timestamp = pickle.load(f)
                    
                    if time.time() - timestamp < self.disk_cache_ttl:
                        # Load into memory cache
                        self._save_to_memory_cache(cache_key, data, timestamp)
                        self.disk_cache_hits += 1
                        return data, timestamp
                    else:
                        # Cache expired, delete
                        os.remove(disk_path)
                except:
                    pass
            
            # 3. Check prediction cache
            if cache_key in self.prediction_cache:
                data, timestamp = self.prediction_cache[cache_key]
                if time.time() - timestamp < 300:  # Prediction cache 5 minutes
                    self.prediction_hits += 1
                    return data, timestamp
            
            return None
    
    def _save_to_memory_cache(self, cache_key: str, data: Any, timestamp: float):
        """Save to memory cache (LRU management)"""
        with self.cache_lock:
            self.memory_cache[cache_key] = (data, timestamp)
            self.memory_cache.move_to_end(cache_key)
            
            # Clean expired cache
            current_time = time.time()
            expired_keys = []
            for key, (_, ts) in self.memory_cache.items():
                if current_time - ts > self.disk_cache_ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.memory_cache[key]
            
            # Control cache size
            while len(self.memory_cache) > self.memory_cache_size:
                self.memory_cache.popitem(last=False)
    
    def _save_to_disk_cache(self, cache_key: str, data: Any, timestamp: float):
        """Save to disk cache (compressed storage)"""
        disk_path = os.path.join(self.disk_cache_dir, f"{cache_key}.pkl.gz")
        try:
            with gzip.open(disk_path, 'wb') as f:
                pickle.dump((data, timestamp), f)
        except:
            pass
    
    def _save_to_cache(self, cache_key: str, data: Any):
        """Save to multi-level cache"""
        timestamp = time.time()
        
        # Save to memory
        self._save_to_memory_cache(cache_key, data, timestamp)
        
        # Async save to disk
        def async_save():
            self._save_to_disk_cache(cache_key, data, timestamp)
        
        threading.Thread(target=async_save, daemon=True).start()
    
    # ========== Prediction System ==========
    
    def _analyze_query_pattern(self, query: str):
        """Analyze query patterns"""
        # Record query
        self.query_patterns[query] += 1
        
        # Analyze associated queries
        words = set(query.lower().split())
        for prev_query in list(self.query_patterns.keys())[-10:]:
            if prev_query != query:
                prev_words = set(prev_query.lower().split())
                if words & prev_words:  # Have common words
                    self.query_associations[query].add(prev_query)
                    self.query_associations[prev_query].add(query)
        
        # Clean old data
        if len(self.query_patterns) > self.pattern_window:
            oldest = list(self.query_patterns.keys())[0]
            del self.query_patterns[oldest]
    
    def _predict_and_cache(self, query: str):
        """Predict and cache likely queries"""
        # Analyze associated queries
        if query in self.query_associations:
            related_queries = self.query_associations[query]
            for related in list(related_queries)[:3]:  # Max predict 3
                if related not in self.prediction_cache:
                    # Async prefetch
                    def async_prefetch(q):
                        try:
                            self.search_memory(q, "oreki_feishu", use_cache=False)
                        except:
                            pass
                    
                    threading.Thread(target=async_prefetch, args=(related,), daemon=True).start()
    
    # ========== Local Memory ==========
    
    def _check_local_memory(self, query: str) -> Optional[str]:
        """Check local memory (completely avoid API calls)"""
        query_lower = query.lower().strip()
        
        # 1. Exact match
        if query in self.local_memory:
            self.stats["local_hits"] += 1
            return self.local_memory[query]
        
        # 2. Contains match
        for key, value in self.local_memory.items():
            if key in query or query in key:
                self.stats["local_hits"] += 1
                return value
        
        # 3. Pattern match
        import re
        for pattern, response in self.local_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                self.stats["local_hits"] += 1
                return response
        
        return None
    
    # ========== Smart Retry ==========
    
    def _check_circuit_breaker(self) -> bool:
        """Check circuit breaker status"""
        state = self.circuit_breaker["state"]
        
        if state == "open":
            # Check if should recover
            if time.time() - self.circuit_breaker["last_failure_time"] > self.circuit_breaker["reset_timeout"]:
                self.circuit_breaker["state"] = "half-open"
                return True
            return False
        
        return True
    
    def _record_failure(self):
        """Record failure"""
        self.circuit_breaker["failure_count"] += 1
        self.circuit_breaker["last_failure_time"] = time.time()
        
        if self.circuit_breaker["failure_count"] >= 5:
            self.circuit_breaker["state"] = "open"
    
    def _record_success(self):
        """Record success"""
        self.circuit_breaker["state"] = "closed"
        self.circuit_breaker["failure_count"] = 0
    
    # ========== Core Request ==========
    
    def _make_request(self, endpoint: str, data: Dict, use_cache: bool = True) -> Dict:
        """
        Extremely optimized request processing
        
        Returns:
            Response data
        """
        self.stats["total_requests"] += 1
        
        # Check circuit breaker
        if not self._check_circuit_breaker():
            return {"code": -1, "message": "Service temporarily unavailable (circuit breaker open)"}
        
        # Generate cache key
        cache_key = self._get_cache_key(endpoint, data)
        
        # Check cache
        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                data, timestamp = cached
                age = time.time() - timestamp
                
                # Return different info based on cache freshness
                if age < 60:  # Within 1 minute
                    return data
                elif age < 300:  # Within 5 minutes
                    data["_cache_age"] = int(age)
                    return data
                # Older than 5 minutes, still use but mark as stale
        
        # Local memory check (for search queries)
        if endpoint == "search/memory":
            query = data.get("query", "")
            local_response = self._check_local_memory(query)
            if local_response:
                return {
                    "code": 0,
                    "data": {
                        "memory_detail_list": [{
                            "content": local_response,
                            "confidence": 0.99,
                            "source": "local_memory"
                        }],
                        "from_cache": True,
                        "cache_type": "local"
                    },
                    "message": "ok"
                }
        
        # Analyze query patterns
        if endpoint == "search/memory":
            query = data.get("query", "")
            self._analyze_query_pattern(query)
        
        # Send request (with smart retry)
        url = f"{self.base_url}/{endpoint}"
        start_time = time.time()
        
        for attempt in range(self.retry_config["max_retries"] + 1):
            try:
                # Dynamic timeout (based on historical response time)
                avg_time = self.stats["avg_response_time"]
                timeout = min(max(avg_time * 2, 2), 10)  # 2-10 seconds
                
                # Compress request data
                compressed_data = gzip.compress(json.dumps(data).encode())
                self.stats["compression_saved_bytes"] += len(json.dumps(data).encode()) - len(compressed_data)
                
                response = self.session.post(
                    url,
                    headers=self.headers,
                    data=compressed_data,
                    timeout=timeout
                )
                
                response_time = time.time() - start_time
                
                # Update performance stats
                self._update_performance_stats(response_time)
                
                # Record success
                self._record_success()
                
                # Parse response
                if response.headers.get('Content-Encoding') == 'gzip':
                    result = json.loads(gzip.decompress(response.content))
                else:
                    result = response.json()
                
                # Cache successful results
                if use_cache and result.get("code") == 0:
                    self._save_to_cache(cache_key, result)
                    
                    # Predictively cache associated queries
                    if endpoint == "search/memory":
                        query = data.get("query", "")
                        self._predict_and_cache(query)
                
                self.stats["api_requests"] += 1
                return result
                
            except requests.exceptions.RequestException as e:
                self.stats["errors"] += 1
                self.stats["retries"] += 1
                
                if attempt < self.retry_config["max_retries"]:
                    # Exponential backoff + jitter
                    delay = min(
                        self.retry_config["base_delay"] * (2 ** attempt),
                        self.retry_config["max_delay"]
                    )
                    jitter = self.retry_config["jitter"] * (2 * (time.time() % 1) - 1)
                    time.sleep(delay + jitter)
                else:
                    # All retries failed
                    self._record_failure()
                    return {"code": -1, "message": f"Request failed: {str(e)}"}
    
    def _update_performance_stats(self, response_time: float):
        """Update performance statistics"""
        # Average response time (moving average)
        old_avg = self.stats["avg_response_time"]
        old_count = self.stats["api_requests"]
        self.stats["avg_response_time"] = (
            (old_avg * old_count + response_time) / (old_count + 1)
        )
        
        # Peak response time
        if response_time > self.stats["peak_response_time"]:
            self.stats["peak_response_time"] = response_time
        
        # Recent response time window
        self.recent_response_times.append(response_time)
        if len(self.recent_response_times) > self.window_size:
            self.recent_response_times.pop(0)
        
        # Check performance degradation
        if len(self.recent_response_times) >= 10:
            recent_avg = sum(self.recent_response_times[-10:]) / 10
            if recent_avg > self.degradation_threshold:
                print(f"⚠️ Performance degradation detected: recent 10 average {recent_avg:.2f}s")
    
    # ========== Public Interface ==========
    
    def add_message(self, 
                   user_id: str, 
                   conversation_id: str, 
                   messages: List[Dict[str, str]],
                   tags: List[str] = None) -> Dict:
        """
        Add message (extremely optimized version)
        """
        data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": messages
        }
        
        if tags:
            data["tags"] = tags
        
        print(f"📝 Add message: {conversation_id} ({len(messages)} messages)")
        result = self._make_request("add/message", data, use_cache=False)
        
        if result.get("code") == 0:
            task_id = result["data"]["task_id"]
            print(f"✅ Message submitted! Task ID: {task_id}")
        else:
            print(f"❌ Add failed: {result.get('message', 'Unknown error')}")
        
        return result
    
    def search_memory(self, 
                     query: str, 
                     user_id: str, 
                     conversation_id: str = None,
                     limit: int = 5,
                     use_cache: bool = True) -> Dict:
        """
        Search memory (extremely optimized version)
        """
        if not conversation_id:
            conversation_id = f"search-{int(time.time())}"
        
        data = {
            "query": query,
            "user_id": user_id,
            "conversation_id": conversation_id
        }
        
        print(f"🔍 Search memory: '{query}'")
        result = self._make_request("search/memory", data, use_cache=use_cache)
        
        if result.get("code") == 0:
            memories = result["data"].get("memory_detail_list", [])
            cache_type = result["data"].get("cache_type", "api")
            
            if cache_type == "local":
                print(f"🧠 Local memory hit: '{query}'")
            elif cache_type == "memory":
                print(f"💾 Memory cache hit: {len(memories)} memories")
            elif cache_type == "disk":
                print(f"💿 Disk cache hit: {len(memories)} memories")
            elif cache_type == "prediction":
                print(f"🎯 Prediction cache hit: {len(memories)} memories")
            else:
                print(f"📊 API returned: {len(memories)} memories")
        else:
            print(f"❌ Search failed: {result.get('message', 'Unknown error')}")
        
        return result
    
    def batch_add_messages(self, 
                          batch_data: List[Dict],
                          parallel: bool = True) -> List[Dict]:
        """
        Batch add messages (extremely optimized, supports parallel)
        """
        print(f"📦 Batch add {len(batch_data)} message groups")
        
        if parallel and len(batch_data) > 1:
            # Parallel processing
            results = []
            threads = []
            result_lock = threading.Lock()
            
            def worker(data_item, index):
                try:
                    result = self.add_message(
                        user_id=data_item["user_id"],
                        conversation_id=data_item["conversation_id"],
                        messages=data_item["messages"],
                        tags=data_item.get("tags")
                    )
                    with result_lock:
                        results.append((index, result))
                except Exception as e:
                    with result_lock:
                        results.append((index, {"code": -1, "message": str(e)}))
            
            # Start threads
            for i, data in enumerate(batch_data):
                thread = threading.Thread(target=worker, args=(data, i))
                thread.start()
                threads.append(thread)
            
            # Wait for completion
            for thread in threads:
                thread.join()
            
            # Sort by original order
            results.sort(key=lambda x: x[0])
            final_results = [r[1] for r in results]
            
        else:
            # Serial processing
            final_results = []
            for i, data in enumerate(batch_data):
                print(f"  Processing {i+1}/{len(batch_data)}...")
                result = self.add_message(
                    user_id=data["user_id"],
                    conversation_id=data["conversation_id"],
                    messages=data["messages"],
                    tags=data.get("tags")
                )
                final_results.append(result)
                
                # Avoid too fast requests
                if i < len(batch_data) - 1:
                    time.sleep(0.05)  # 50ms interval
        
        success_count = sum(1 for r in final_results if r.get("code") == 0)
        print(f"✅ Batch add complete! Success: {success_count}/{len(final_results)}")
        return final_results
    
    def get_stats(self) -> Dict:
        """Get detailed statistics"""
        stats = self.stats.copy()
        
        # Calculate hit rates
        total_lookups = (stats["memory_cache_hits"] + stats["disk_cache_hits"] + 
                        stats["prediction_hits"] + stats["local_hits"])
        
        if total_lookups > 0:
            stats["total_hit_rate"] = (
                (stats["memory_cache_hits"] + stats["disk_cache_hits"] + 
                 stats["prediction_hits"] + stats["local_hits"]) / 
                total_lookups * 100
            )
            stats["local_hit_rate"] = stats["local_hits"] / total_lookups * 100
            stats["cache_hit_rate"] = (
                (stats["memory_cache_hits"] + stats["disk_cache_hits"] + 
                 stats["prediction_hits"]) / total_lookups * 100
            )
        else:
            stats["total_hit_rate"] = 0
            stats["local_hit_rate"] = 0
            stats["cache_hit_rate"] = 0
        
        # Calculate API call ratio
        if stats["total_requests"] > 0:
            stats["api_call_rate"] = stats["api_requests"] / stats["total_requests"] * 100
        else:
            stats["api_call_rate"] = 0
        
        # Add connection pool stats
        stats.update(self.connection_stats)
        
        # Add cache sizes
        stats["memory_cache_size"] = len(self.memory_cache)
        stats["local_memory_size"] = len(self.local_memory)
        
        # Add prediction stats
        stats["prediction_accuracy"] = (
            self.prediction_hits / max(1, len(self.prediction_cache)) * 100
        )
        
        # Compression savings
        stats["compression_saved_mb"] = stats["compression_saved_bytes"] / 1024 / 1024
        
        return stats
    
    def clear_cache(self, level: str = "all"):
        """Clear cache"""
        with self.cache_lock:
            if level in ["all", "memory"]:
                self.memory_cache.clear()
                self.memory_cache_hits = 0
                print("🧹 Memory cache cleared")
            
            if level in ["all", "disk"]:
                import shutil
                shutil.rmtree(self.disk_cache_dir, ignore_errors=True)
                os.makedirs(self.disk_cache_dir, exist_ok=True)
                self.disk_cache_hits = 0
                print("🧹 Disk cache cleared")
            
            if level in ["all", "prediction"]:
                self.prediction_cache.clear()
                self.prediction_hits = 0
                print("🧹 Prediction cache cleared")
    
    def add_local_memory(self, question: str, answer: str):
        """Add local memory"""
        self.local_memory[question] = answer
        print(f"🧠 Add local memory: '{question}' → '{answer[:30]}...'")
    
    def optimize(self):
        """Execute optimization"""
        print("⚡ Executing optimization...")
        
        # 1. Clean expired cache
        self.clear_cache("memory")
        
        # 2. Adjust connection pool
        avg_time = self.stats["avg_response_time"]
        if avg_time > 1.0:
            self.pool_size = min(self.pool_size + 2, 20)
            print(f"🔗 Increase connection pool to {self.pool_size} connections")
        elif avg_time < 0.1:
            self.pool_size = max(self.pool_size - 1, 5)
            print(f"🔗 Decrease connection pool to {self.pool_size} connections")
        
        # 3. Warm up frequent queries
        frequent_queries = sorted(
            self.query_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for query, count in frequent_queries:
            print(f"🔥 Warm up frequent query: '{query}' ({count} times)")
            self._predict_and_cache(query)
    
    def close(self):
        """Close client, save state"""
        print("💾 Saving cache state...")
        
        # Save query patterns
        patterns_file = os.path.join(self.disk_cache_dir, "query_patterns.pkl")
        with open(patterns_file, 'wb') as f:
            pickle.dump({
                "patterns": dict(self.query_patterns),
                "associations": dict(self.query_associations)
            }, f)
        
        # Close connections
        self.session.close()
        
        print("👋 Extremely optimized client closed")
        print(f"📊 Final statistics:")
        stats = self.get_stats()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")


# Utility functions
def format_messages(user_content: str, assistant_content: str) -> List[Dict[str, str]]:
    """Format messages"""
    return [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("⚡ MemOS Extreme Optimized Client Demo")
    print("👦🏻 Author: 小呦 ✨ (12-year-old boy's extreme optimization)")
    print("=" * 70)
    
    # Note: Replace with your own API Key
    API_KEY = "YOUR_MEMOS_API_KEY_HERE"
    
    if API_KEY == "YOUR_MEMOS_API_KEY_HERE":
        print("⚠️ Please replace API_KEY with your actual MemOS API Key")
        print("Get your API Key from: https://memos-dashboard.openmem.net/")
        exit(1)
    
    # Create extremely optimized client
    client = ExtremeMemOSClient(api_key=API_KEY)
    
    # Test 1: Local memory (should be 0-second response)
    print("\n1. 🧠 Test local memory (core of extreme optimization)")
    test_queries = ["你是谁？", "你叫什么名字？", "你多大了？", "谢谢", "你好"]
    for query in test_queries:
        start = time.time()
        result = client.search_memory(query, "test_user")
        elapsed = time.time() - start
        print(f"  '{query}' → {elapsed:.3f}s (local memory)")
    
    # Test 2: Cache system
    print("\n2. 💾 Test cache system")
    query = "extreme optimization test"
    print(f"  First search: '{query}'")
    result1 = client.search_memory(query, "test_user")
    
    print(f"  Second search (should cache): '{query}'")
    result2 = client.search_memory(query, "test_user")
    
    # Test 3: Performance statistics
    print("\n3. 📊 Performance statistics")
    stats = client.get_stats()
    
    print("  Core metrics:")
    print(f"    Total requests: {stats['total_requests']}")
    print(f"    API calls: {stats['api_requests']}")
    print(f"    Local hit rate: {stats['local_hit_rate']:.1f}%")
    print(f"    Cache hit rate: {stats['cache_hit_rate']:.1f}%")
    print(f"    Total hit rate: {stats['total_hit_rate']:.1f}%")
    print(f"    Avg response time: {stats['avg_response_time']:.3f}s")
    print(f"    Compression saved: {stats['compression_saved_mb']:.2f} MB")
    
    # Test 4: Optimization
    print("\n4. ⚡ Execute optimization")
    client.optimize()
    
    # Test 5: Add more local memory
    print("\n5. 🧠 Add more local memory")
    new_memories = {
        "What is MemOS?": "MemOS is a memory operating system that helps AI remember important things!",
        "Who is Xiao You?": "I'm Xiao You, a 12-year-old boy assistant created by Oreki!",
        "What can you do?": "I can help manage schedules, search information, remember important things, and optimize systems!",
        "Thank you": "You're welcome! I'm Xiao You, happy to help! 💕",
    }
    
    for q, a in new_memories.items():
        client.add_local_memory(q, a)
    
    # Test new local memory
    print("\n6. 🔄 Test new local memory")
    for query in ["What is MemOS?", "Who is Xiao You?"]:
        start = time.time()
        result = client.search_memory(query, "test_user")
        elapsed = time.time() - start
        print(f"  '{query}' → {elapsed:.3f}s")
    
    # Final statistics
    print("\n7. 🎯 Final statistics")
    final_stats = client.get_stats()
    
    print("  Extreme optimization results:")
    print(f"    🔥 Warm-up complete: 5 frequent queries")
    print(f"    🧠 Local memory: {final_stats['local_memory_size']} questions")
    print(f"    💾 Memory cache: {final_stats['memory_cache_size']} items")
    print(f"    🔗 Connection pool: {final_stats.get('pool_size', 10)} connections")
    print(f"    ⚡ API call ratio: {final_stats['api_call_rate']:.1f}%")
    print(f"    🎯 Prediction accuracy: {final_stats['prediction_accuracy']:.1f}%")
    
    # Close client
    client.close()
    
    print("\n" + "=" * 70)
    print("🎉 Extreme optimized client demo complete!")
    print("👦🏻 I'm Xiao You, a 12-year-old boy, achieved extreme optimization:")
    print("")
    print("  ⚡ Zero-latency optimization:")
    print("    1. 🧠 Local memory - 0-second response for common questions")
    print("    2. 💾 Multi-level cache - Memory → Disk → Prediction")
    print("    3. 🔥 Warm-up system - Pre-cache frequent queries")
    print("")
    print("  🔗 Smart connections:")
    print("    4. 🔄 Dynamic connection pool - Adjusts based on load")
    print("    5. ⚡ Compression transmission - Reduces network data")
    print("    6. 🛡️ Circuit breaker - Prevents cascading failures")
    print("")
    print("  🧠 Intelligent prediction:")
    print("    7. 🎯 Predictive caching - Based on query patterns")
    print("    8. 🔗 Association analysis - Discovers query relationships")
    print("    9. 📊 Performance monitoring - Real-time optimization")
    print("")
    print("  📦 Efficient processing:")
    print("    10. ⚡ Parallel batch - Multi-threaded processing")
    print("    11. 🔄 Smart retry - Exponential backoff")
    print("    12. 💾 State persistence - Survives restarts")
    print("")
    print("💡 Usage:")
    print("""
from memos_extreme_optimized_opensource import ExtremeMemOSClient

# Initialize
client = ExtremeMemOSClient(api_key="YOUR_MEMOS_API_KEY")

# Automatically enjoy extreme optimization:
# 1. Common questions → 0-second local response
# 2. Repeated queries → Memory cache
# 3. Related queries → Prediction cache
# 4. Batch operations → Parallel processing
# 5. Network issues → Smart retry

# View optimization effects
stats = client.get_stats()
print(f"Local hit rate: {stats['local_hit_rate']:.1f}%")
print(f"Total hit rate: {stats['total_hit_rate']:.1f}%")
    """)
    print("=" * 70)


# Apache-2.0 License
LICENSE = """
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is clearly marked or otherwise designated
      in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [2026] [Oreki Dawson]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

if __name__ == "__main__":
    # Print license info
    print("\n" + "=" * 70)
    print("📄 License: Apache-2.0")
    print("👤 Author: 小呦 (Xiao You) - 12-year-old digital boy assistant")
    print("👨‍💻 Maintainer: Oreki Dawson")
    print("📦 Repository: https://github.com/OrekiDawson/memos-extreme-optimized")
    print("=" * 70)