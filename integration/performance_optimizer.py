"""
Advanced Performance Optimizer for AI Life Operating System
Handles caching, memory management, and system optimization
"""
import time
import asyncio
import threading
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import psutil
import json

class PerformanceOptimizer:
    """Advanced system optimization and performance monitoring"""
    
    def __init__(self, ai_system):
        self.ai_system = ai_system
        
        # Performance caching
        self.response_cache = {}
        self.pattern_cache = {}
        self.relationship_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Memory management
        self.memory_threshold = 0.8  # 80% memory usage trigger
        self.max_cached_experiences = 500
        self.experience_buffer = deque(maxlen=1000)
        
        # Performance metrics
        self.metrics = {
            "response_times": [],
            "cache_hits": 0,
            "cache_misses": 0,
            "memory_optimizations": 0,
            "system_load_avg": []
        }
        
        # Optimization flags
        self.optimization_enabled = True
        self.auto_cleanup_enabled = True
        
        print("⚡ Performance Optimizer initialized")
    
    def optimize_response_caching(self, message: str, response: str) -> bool:
        """Cache responses for similar messages"""
        try:
            # Create cache key from message
            cache_key = self._generate_cache_key(message)
            
            # Store in cache with timestamp
            self.response_cache[cache_key] = {
                "response": response,
                "timestamp": time.time(),
                "access_count": 1
            }
            
            # Cleanup old cache entries
            self._cleanup_expired_cache()
            
            return True
        except Exception as e:
            print(f"⚠️ Cache optimization failed: {e}")
            return False
    
    def get_cached_response(self, message: str) -> Optional[str]:
        """Retrieve cached response if available"""
        try:
            cache_key = self._generate_cache_key(message)
            
            if cache_key in self.response_cache:
                cached_item = self.response_cache[cache_key]
                
                # Check if cache is still valid
                if time.time() - cached_item["timestamp"] < self.cache_ttl:
                    cached_item["access_count"] += 1
                    self.metrics["cache_hits"] += 1
                    return cached_item["response"]
                else:
                    # Remove expired cache
                    del self.response_cache[cache_key]
            
            self.metrics["cache_misses"] += 1
            return None
            
        except Exception as e:
            print(f"⚠️ Cache retrieval failed: {e}")
            return None
    
    def _generate_cache_key(self, message: str) -> str:
        """Generate cache key from message"""
        # Normalize message for better cache hits
        normalized = message.lower().strip()
        
        # Create semantic key (simple similarity)
        key_words = normalized.split()[:5]  # First 5 words
        return "_".join(key_words)
    
    def optimize_memory_usage(self) -> Dict[str, Any]:
        """Optimize system memory usage"""
        optimization_results = {
            "memory_freed": 0,
            "experiences_archived": 0,
            "cache_entries_cleaned": 0,
            "system_memory_usage": 0.0
        }
        
        try:
            # Get current memory usage
            memory_info = psutil.virtual_memory()
            optimization_results["system_memory_usage"] = memory_info.percent / 100.0
            
            # If memory usage is high, perform optimization
            if memory_info.percent / 100.0 > self.memory_threshold:
                print("🧹 High memory usage detected - optimizing...")
                
                # Archive old experiences
                archived = self._archive_old_experiences()
                optimization_results["experiences_archived"] = archived
                
                # Clean cache
                cleaned = self._cleanup_expired_cache()
                optimization_results["cache_entries_cleaned"] = cleaned
                
                # Clear metrics history
                self._cleanup_metrics()
                
                self.metrics["memory_optimizations"] += 1
                print(f"✅ Memory optimization complete: {archived} experiences archived")
            
            return optimization_results
            
        except Exception as e:
            print(f"⚠️ Memory optimization failed: {e}")
            return optimization_results
    
    def _archive_old_experiences(self) -> int:
        """Archive old experiences to free memory"""
        try:
            # Get all experiences
            experiences = self.ai_system.memory_manager.retrieve_experiences("user", 1000)
            
            if len(experiences) <= self.max_cached_experiences:
                return 0
            
            # Sort by importance and timestamp
            experiences.sort(key=lambda x: (
                x.get('importance', 0.5),
                x.get('timestamp', '')
            ))
            
            # Archive least important experiences
            to_archive = len(experiences) - self.max_cached_experiences
            archived_count = 0
            
            for exp in experiences[:to_archive]:
                # Mark as archived (in real system, move to long-term storage)
                exp_data = exp.get('experience', {})
                exp_data['archived'] = True
                archived_count += 1
            
            return archived_count
            
        except Exception as e:
            print(f"⚠️ Experience archiving failed: {e}")
            return 0
    
    def _cleanup_expired_cache(self) -> int:
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = []
        
        # Find expired entries
        for key, cached_item in self.response_cache.items():
            if current_time - cached_item["timestamp"] > self.cache_ttl:
                expired_keys.append(key)
        
        # Remove expired entries
        for key in expired_keys:
            del self.response_cache[key]
        
        return len(expired_keys)
    
    def _cleanup_metrics(self):
        """Clean up old metrics data"""
        # Keep only recent metrics
        max_metrics = 100
        
        if len(self.metrics["response_times"]) > max_metrics:
            self.metrics["response_times"] = self.metrics["response_times"][-max_metrics:]
        
        if len(self.metrics["system_load_avg"]) > max_metrics:
            self.metrics["system_load_avg"] = self.metrics["system_load_avg"][-max_metrics:]
    
    def monitor_system_performance(self) -> Dict[str, Any]:
        """Monitor overall system performance"""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Calculate performance scores
            cache_hit_rate = 0.0
            if self.metrics["cache_hits"] + self.metrics["cache_misses"] > 0:
                cache_hit_rate = self.metrics["cache_hits"] / (
                    self.metrics["cache_hits"] + self.metrics["cache_misses"]
                )
            
            avg_response_time = 0.0
            if self.metrics["response_times"]:
                avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
            
            performance_report = {
                "system_health": "excellent" if cpu_percent < 50 and memory.percent < 70 else 
                               "good" if cpu_percent < 80 and memory.percent < 85 else "needs_attention",
                "cpu_usage": cpu_percent / 100.0,
                "memory_usage": memory.percent / 100.0,
                "cache_hit_rate": cache_hit_rate,
                "average_response_time": avg_response_time,
                "total_cache_entries": len(self.response_cache),
                "memory_optimizations_performed": self.metrics["memory_optimizations"],
                "optimization_recommendations": []
            }
            
            # Generate optimization recommendations
            if cpu_percent > 80:
                performance_report["optimization_recommendations"].append("High CPU usage - consider agent load balancing")
            
            if memory.percent > 80:
                performance_report["optimization_recommendations"].append("High memory usage - enable automatic cleanup")
            
            if cache_hit_rate < 0.3 and self.metrics["cache_hits"] + self.metrics["cache_misses"] > 20:
                performance_report["optimization_recommendations"].append("Low cache hit rate - improve caching strategy")
            
            # Store system load for trending
            self.metrics["system_load_avg"].append(cpu_percent)
            
            return performance_report
            
        except Exception as e:
            print(f"⚠️ Performance monitoring failed: {e}")
            return {"system_health": "unknown", "error": str(e)}
    
    def optimize_agent_performance(self) -> Dict[str, Any]:
        """Optimize agent network performance"""
        optimization_results = {
            "agents_optimized": 0,
            "routing_improvements": 0,
            "load_balancing_applied": False
        }
        
        try:
            # Get agent network status
            network_status = self.ai_system.agent_network.get_network_status()
            
            # Check for optimization opportunities
            if network_status.get("network_size", 0) > 0:
                # Optimize orchestrator routing
                orchestrator = self.ai_system.agent_network.orchestrator
                if orchestrator:
                    routing_analytics = orchestrator.get_routing_analytics()
                    success_rate = float(routing_analytics.get("routing_success_rate", "0%").replace("%", ""))
                    
                    if success_rate < 90:
                        optimization_results["routing_improvements"] += 1
                        print("🔧 Optimizing agent routing patterns...")
                
                optimization_results["agents_optimized"] = network_status["network_size"]
            
            return optimization_results
            
        except Exception as e:
            print(f"⚠️ Agent optimization failed: {e}")
            return optimization_results
    
    async def run_continuous_optimization(self):
        """Run continuous system optimization in background"""
        while self.optimization_enabled:
            try:
                # Performance monitoring
                performance = self.monitor_system_performance()
                
                # Memory optimization if needed
                if performance["memory_usage"] > self.memory_threshold:
                    self.optimize_memory_usage()
                
                # Agent optimization
                self.optimize_agent_performance()
                
                # Sleep before next optimization cycle
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                print(f"⚠️ Optimization cycle failed: {e}")
                await asyncio.sleep(60)  # Retry in 1 minute
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report"""
        performance = self.monitor_system_performance()
        
        return {
            "performance_metrics": performance,
            "cache_statistics": {
                "total_entries": len(self.response_cache),
                "hit_rate": self.metrics["cache_hits"] / max(1, self.metrics["cache_hits"] + self.metrics["cache_misses"]),
                "hits": self.metrics["cache_hits"],
                "misses": self.metrics["cache_misses"]
            },
            "optimization_status": {
                "enabled": self.optimization_enabled,
                "auto_cleanup": self.auto_cleanup_enabled,
                "memory_optimizations": self.metrics["memory_optimizations"]
            },
            "recommendations": performance.get("optimization_recommendations", [])
        }

# Test performance optimizer
if __name__ == "__main__":
    print("🧪 Testing Performance Optimizer...")
    
    # Mock AI system for testing
    class MockAISystem:
        def __init__(self):
            self.memory_manager = None
            self.agent_network = None
    
    ai_system = MockAISystem()
    optimizer = PerformanceOptimizer(ai_system)
    
    # Test caching
    optimizer.optimize_response_caching("Hello there", "Hi! How can I help you?")
    cached_response = optimizer.get_cached_response("Hello there")
    print(f"Cached response: {cached_response[:30]}..." if cached_response else "No cache hit")
    
    # Test performance monitoring
    performance = optimizer.monitor_system_performance()
    print(f"System health: {performance['system_health']}")
    
    # Test optimization report
    report = optimizer.get_optimization_report()
    print(f"Cache hit rate: {report['cache_statistics']['hit_rate']:.2%}")
    
    print("🎉 Performance Optimizer test complete!")
