"""
System Health Monitor for AI Life Operating System
Real-time monitoring, diagnostics, and alert system
"""

import time
import threading
from typing import Dict, Any, List, Callable
from datetime import datetime, timedelta
from collections import deque
import json

class SystemHealthMonitor:
    """Comprehensive system health monitoring and alerting"""
    
    def __init__(self, ai_system):
        self.ai_system = ai_system
        
        # Health metrics storage
        self.health_history = deque(maxlen=100)
        self.alert_callbacks: List[Callable] = []
        
        # Health thresholds
        self.thresholds = {
            "memory_usage_critical": 0.9,
            "memory_usage_warning": 0.8,
            "response_time_critical": 10.0,  # seconds
            "response_time_warning": 5.0,
            "agent_failure_rate_critical": 0.3,
            "agent_failure_rate_warning": 0.1
        }
        
        # Monitoring state
        self.monitoring_active = False
        self.last_health_check = 0
        self.health_check_interval = 60  # seconds
        
        # Alert state
        self.active_alerts = {}
        self.alert_cooldown = 300  # 5 minutes
        
        print("🏥 System Health Monitor initialized")
    
    def start_monitoring(self):
        """Start continuous health monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("🏥 Health monitoring started")
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        print("🏥 Health monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Perform comprehensive health check
                health_data = self.perform_health_check()
                
                # Store health data
                self.health_history.append({
                    "timestamp": time.time(),
                    "health_data": health_data
                })
                
                # Check for alerts
                self._check_health_alerts(health_data)
                
                # Sleep until next check
                time.sleep(self.health_check_interval)
                
            except Exception as e:
                print(f"⚠️ Health monitoring error: {e}")
                time.sleep(30)  # Short sleep before retry
    
    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive system health check"""
        health_data = {
            "timestamp": time.time(),
            "overall_health": "healthy",
            "components": {},
            "metrics": {},
            "issues": []
        }
        
        try:
            # Check AI system status
            system_status = self.ai_system.get_status()
            health_data["components"]["ai_system"] = self._check_ai_system_health(system_status)
            
            # Check memory system health
            health_data["components"]["memory_system"] = self._check_memory_health()
            
            # Check agent network health
            health_data["components"]["agent_network"] = self._check_agent_network_health()
            
            # Check proactive intelligence health
            health_data["components"]["proactive_intelligence"] = self._check_proactive_intelligence_health()
            
            # Calculate overall health
            health_data["overall_health"] = self._calculate_overall_health(health_data["components"])
            
            # Extract key metrics
            health_data["metrics"] = self._extract_key_metrics(system_status)
            
            self.last_health_check = time.time()
            
        except Exception as e:
            health_data["overall_health"] = "error"
            health_data["issues"].append(f"Health check failed: {str(e)}")
        
        return health_data
    
    def _check_ai_system_health(self, system_status: Dict[str, Any]) -> Dict[str, Any]:
        """Check AI system component health"""
        component_health = {
            "status": "healthy",
            "metrics": {},
            "issues": []
        }
        
        try:
            # Check if system is running
            if not system_status.get("system_running", False):
                component_health["status"] = "critical"
                component_health["issues"].append("System not running")
            
            # Check memory usage
            total_memories = system_status.get("total_memories", 0)
            component_health["metrics"]["total_memories"] = total_memories
            
            if total_memories > 1000:
                component_health["issues"].append("High memory usage - consider optimization")
            
            # Check patterns
            patterns_detected = system_status.get("patterns_detected", 0)
            pattern_confidence = system_status.get("pattern_confidence", 0.0)
            
            component_health["metrics"]["patterns_detected"] = patterns_detected
            component_health["metrics"]["pattern_confidence"] = pattern_confidence
            
            if pattern_confidence > 0 and patterns_detected == 0:
                component_health["issues"].append("Pattern recognition inconsistency")
            
        except Exception as e:
            component_health["status"] = "error"
            component_health["issues"].append(f"AI system check failed: {str(e)}")
        
        return component_health
    
    def _check_memory_health(self) -> Dict[str, Any]:
        """Check memory system health"""
        component_health = {
            "status": "healthy",
            "metrics": {},
            "issues": []
        }
        
        try:
            # Check memory manager
            if hasattr(self.ai_system, 'memory_manager'):
                # Test memory retrieval
                start_time = time.time()
                experiences = self.ai_system.memory_manager.retrieve_experiences("user", 10)
                retrieval_time = time.time() - start_time
                
                component_health["metrics"]["experience_count"] = len(experiences)
                component_health["metrics"]["retrieval_time"] = retrieval_time
                
                if retrieval_time > 2.0:
                    component_health["issues"].append("Slow memory retrieval")
                
                # Check consolidation engine
                if hasattr(self.ai_system.memory_manager, 'consolidation_engine'):
                    component_health["metrics"]["consolidation_engine"] = "available"
                else:
                    component_health["issues"].append("Consolidation engine not linked")
            else:
                component_health["status"] = "critical"
                component_health["issues"].append("Memory manager not found")
                
        except Exception as e:
            component_health["status"] = "error"
            component_health["issues"].append(f"Memory health check failed: {str(e)}")
        
        return component_health
    
    def _check_agent_network_health(self) -> Dict[str, Any]:
        """Check agent network health"""
        component_health = {
            "status": "healthy",
            "metrics": {},
            "issues": []
        }
        
        try:
            if hasattr(self.ai_system, 'agent_network'):
                network_status = self.ai_system.agent_network.get_network_status()
                
                component_health["metrics"]["active_agents"] = network_status.get("network_size", 0)
                
                # Check orchestrator
                if hasattr(self.ai_system.agent_network, 'orchestrator'):
                    orchestrator_status = self.ai_system.agent_network.orchestrator.get_system_status()
                    routing_success = orchestrator_status.get("routing_success_rate", 0)
                    
                    component_health["metrics"]["routing_success_rate"] = routing_success
                    
                    if routing_success < 80:
                        component_health["issues"].append("Low routing success rate")
                else:
                    component_health["issues"].append("Orchestrator not available")
            else:
                component_health["status"] = "critical"
                component_health["issues"].append("Agent network not found")
                
        except Exception as e:
            component_health["status"] = "error"
            component_health["issues"].append(f"Agent network check failed: {str(e)}")
        
        return component_health
    
    def _check_proactive_intelligence_health(self) -> Dict[str, Any]:
        """Check proactive intelligence health"""
        component_health = {
            "status": "healthy",
            "metrics": {},
            "issues": []
        }
        
        try:
            if hasattr(self.ai_system, 'autonomous_assistant'):
                intervention_status = self.ai_system.autonomous_assistant.get_intervention_status()
                
                component_health["metrics"]["autonomous_mode"] = intervention_status.get("autonomous_mode", False)
                component_health["metrics"]["total_interventions"] = intervention_status.get("total_interventions", 0)
                component_health["metrics"]["success_rate"] = intervention_status.get("success_rate", 0)
                
                if not intervention_status.get("autonomous_mode", False):
                    component_health["issues"].append("Autonomous mode disabled")
                
                if intervention_status.get("success_rate", 0) < 0.8:
                    component_health["issues"].append("Low intervention success rate")
            else:
                component_health["issues"].append("Autonomous assistant not available")
                
        except Exception as e:
            component_health["status"] = "error"
            component_health["issues"].append(f"Proactive intelligence check failed: {str(e)}")
        
        return component_health
    
    def _calculate_overall_health(self, components: Dict[str, Any]) -> str:
        """Calculate overall system health from component health"""
        critical_count = 0
        error_count = 0
        issue_count = 0
        
        for component_name, component_data in components.items():
            status = component_data.get("status", "unknown")
            issues = len(component_data.get("issues", []))
            
            if status == "critical":
                critical_count += 1
            elif status == "error":
                error_count += 1
            
            issue_count += issues
        
        # Determine overall health
        if critical_count > 0:
            return "critical"
        elif error_count > 1 or issue_count > 5:
            return "degraded"
        elif error_count > 0 or issue_count > 2:
            return "warning"
        else:
            return "healthy"
    
    def _extract_key_metrics(self, system_status: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key metrics for monitoring"""
        return {
            "total_memories": system_status.get("total_memories", 0),
            "patterns_detected": system_status.get("patterns_detected", 0),
            "pattern_confidence": system_status.get("pattern_confidence", 0.0),
            "total_relationships": system_status.get("total_relationships", 0),
            "autonomous_mode": system_status.get("autonomous_mode", False),
            "proactive_interventions": system_status.get("proactive_interventions", 0)
        }
    
    def _check_health_alerts(self, health_data: Dict[str, Any]):
        """Check health data against alert thresholds"""
        current_time = time.time()
        
        # Check overall health alerts
        overall_health = health_data.get("overall_health", "unknown")
        
        if overall_health in ["critical", "degraded"]:
            alert_id = f"system_health_{overall_health}"
            self._trigger_alert(alert_id, f"System health is {overall_health}", "high", health_data)
        
        # Check component-specific alerts
        for component_name, component_data in health_data.get("components", {}).items():
            issues = component_data.get("issues", [])
            
            if issues:
                alert_id = f"component_{component_name}_issues"
                self._trigger_alert(
                    alert_id, 
                    f"{component_name} has {len(issues)} issues: {issues[0]}", 
                    "medium", 
                    component_data
                )
    
    def _trigger_alert(self, alert_id: str, message: str, severity: str, data: Any):
        """Trigger system alert"""
        current_time = time.time()
        
        # Check if alert is in cooldown
        if alert_id in self.active_alerts:
            last_alert_time = self.active_alerts[alert_id]["timestamp"]
            if current_time - last_alert_time < self.alert_cooldown:
                return  # Skip alert due to cooldown
        
        # Create alert
        alert = {
            "id": alert_id,
            "message": message,
            "severity": severity,
            "timestamp": current_time,
            "data": data
        }
        
        # Store active alert
        self.active_alerts[alert_id] = alert
        
        # Trigger alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"⚠️ Alert callback failed: {e}")
        
        print(f"🚨 ALERT [{severity.upper()}]: {message}")
    
    def register_alert_callback(self, callback: Callable):
        """Register callback for health alerts"""
        self.alert_callbacks.append(callback)
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get current health summary"""
        if not self.health_history:
            return {"status": "no_data", "message": "No health data available"}
        
        latest_health = self.health_history[-1]["health_data"]
        
        summary = {
            "overall_health": latest_health.get("overall_health", "unknown"),
            "last_check": datetime.fromtimestamp(latest_health.get("timestamp", 0)).isoformat(),
            "active_alerts": len(self.active_alerts),
            "component_summary": {},
            "key_metrics": latest_health.get("metrics", {}),
            "monitoring_active": self.monitoring_active
        }
        
        # Summarize component health
        for component_name, component_data in latest_health.get("components", {}).items():
            summary["component_summary"][component_name] = {
                "status": component_data.get("status", "unknown"),
                "issue_count": len(component_data.get("issues", []))
            }
        
        return summary
    
    def get_health_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get health trends over specified time period"""
        cutoff_time = time.time() - (hours * 3600)
        
        recent_health = [
            h for h in self.health_history 
            if h["timestamp"] > cutoff_time
        ]
        
        if not recent_health:
            return {"status": "no_data", "message": f"No health data for last {hours} hours"}
        
        # Calculate trends
        health_counts = {"healthy": 0, "warning": 0, "degraded": 0, "critical": 0, "error": 0}
        
        for health_record in recent_health:
            overall_health = health_record["health_data"].get("overall_health", "unknown")
            if overall_health in health_counts:
                health_counts[overall_health] += 1
        
        total_checks = len(recent_health)
        health_percentages = {
            status: (count / total_checks) * 100 
            for status, count in health_counts.items()
        }
        
        return {
            "period_hours": hours,
            "total_health_checks": total_checks,
            "health_distribution": health_percentages,
            "uptime_percentage": health_percentages.get("healthy", 0) + health_percentages.get("warning", 0),
            "trend": "improving" if health_percentages.get("healthy", 0) > 70 else 
                    "stable" if health_percentages.get("healthy", 0) > 50 else "concerning"
        }

# Test health monitor
if __name__ == "__main__":
    print("🧪 Testing System Health Monitor...")
    
    # Mock AI system for testing
    class MockAISystem:
        def get_status(self):
            return {
                "system_running": True,
                "total_memories": 150,
                "patterns_detected": 25,
                "pattern_confidence": 0.8,
                "total_relationships": 5,
                "autonomous_mode": True,
                "proactive_interventions": 3
            }
    
    ai_system = MockAISystem()
    health_monitor = SystemHealthMonitor(ai_system)
    
    # Test health check
    health_data = health_monitor.perform_health_check()
    print(f"Overall health: {health_data['overall_health']}")
    
    # Test health summary
    health_monitor.health_history.append({
        "timestamp": time.time(),
        "health_data": health_data
    })
    
    summary = health_monitor.get_health_summary()
    print(f"Health summary: {summary['overall_health']} with {summary['active_alerts']} alerts")
    
    print("🎉 System Health Monitor test complete!")
