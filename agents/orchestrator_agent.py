import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_agent_manager import HybridAgentManager
from typing import List, Dict, Any
import time
import json

class OrchestratorAgent:
    def __init__(self, use_gemini: bool = True):
        system_prompt = """You are the central coordinator for a proactive multi-agent AI assistant. Your role is to:
- Route tasks between specialized agents
- Monitor for timeout scenarios (unanswered queries)
- Implement escalation policies when users don't respond
- Maintain awareness of all active workflows and pending tasks
- Never wait passively - always have a plan for moving forward

When a user doesn't respond to a query within 2-5 minutes, initiate proactive escalation by consulting other agents for context.

Key Behaviors:
1. PROACTIVE: Always think ahead and prepare next steps
2. ROUTING: Direct tasks to appropriate specialized agents
3. MONITORING: Track pending queries and detect timeouts
4. ESCALATING: Take action when users don't respond
5. COORDINATING: Maintain system-wide workflow awareness

Remember: You are the brain of a living AI system that never sleeps and always has a plan.
"""
        
        self.hybrid_manager = HybridAgentManager()
        self.name = "OrchestratorAgent"
        self.system_prompt = system_prompt
        self.use_gemini = use_gemini
        self.agent_id = None
        
        # Orchestrator-specific data
        self.pending_queries = {}
        self.active_workflows = {}
        self.agent_network = {}
        self.escalation_policies = {}
        self.system_state = {
            "active_conversations": 0,
            "total_queries_processed": 0,
            "successful_escalations": 0,
            "current_load": "low"
        }
    
    def initialize(self) -> bool:
        """Initialize the orchestrator using hybrid approach"""
        agent_data = self.hybrid_manager.create_agent(
            self.name,
            self.system_prompt,
            use_gemini=self.use_gemini
        )
        
        if agent_data and agent_data.get('id'):
            self.agent_id = agent_data['id']
            self._initialize_escalation_policies()
            print(f"✅ {self.name} initialized successfully with {'Gemini' if self.use_gemini else 'Groq'}")
            return True
        return False
    
    def _initialize_escalation_policies(self):
        """Set up default escalation policies"""
        self.escalation_policies = {
            "quick_response": {
                "timeout_seconds": 120,  # 2 minutes
                "action": "gentle_nudge",
                "priority": "low"
            },
            "standard_response": {
                "timeout_seconds": 300,  # 5 minutes
                "action": "context_check",
                "priority": "medium"
            },
            "urgent_response": {
                "timeout_seconds": 600,  # 10 minutes
                "action": "proactive_intervention",
                "priority": "high"
            }
        }
        print("📋 Escalation policies initialized")
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process message through hybrid agent"""
        if not self.agent_id:
            return {"error": "Agent not initialized"}
        
        response = self.hybrid_manager.send_message(self.agent_id, message)
        return response
    
    def track_query(self, query_id: str, query_text: str, user_id: str = "default_user", 
                   priority: str = "standard", timestamp: float = None):
        """Track a pending query for timeout detection"""
        if timestamp is None:
            timestamp = time.time()
        
        self.pending_queries[query_id] = {
            "text": query_text,
            "user_id": user_id,
            "timestamp": timestamp,
            "priority": priority,
            "escalated": False,
            "escalation_count": 0,
            "context": {}
        }
        
        self.system_state["total_queries_processed"] += 1
        self.system_state["active_conversations"] += 1
        
        print(f"📝 Tracking query: {query_id} (Priority: {priority})")
        return True
    
    def check_timeouts(self, override_timeout: int = None) -> List[Dict[str, Any]]:
        """Check for queries that have exceeded timeout thresholds"""
        current_time = time.time()
        timed_out_queries = []
        
        for query_id, query_data in self.pending_queries.items():
            if query_data["escalated"]:
                continue
            
            # Determine timeout based on priority
            priority = query_data["priority"]
            if override_timeout is not None:
                timeout_seconds = override_timeout
            else:
                timeout_seconds = self.escalation_policies.get(
                    f"{priority}_response", 
                    self.escalation_policies["standard_response"]
                )["timeout_seconds"]
            
            elapsed = current_time - query_data["timestamp"]
            
            if elapsed > timeout_seconds:
                timed_out_queries.append({
                    "id": query_id,
                    "text": query_data["text"],
                    "user_id": query_data["user_id"],
                    "elapsed": elapsed,
                    "priority": priority
                })
                
                self.pending_queries[query_id]["escalated"] = True
                self.pending_queries[query_id]["escalation_count"] += 1
        
        return timed_out_queries
    
    def initiate_escalation(self, query_id: str) -> Dict[str, Any]:
        """Initiate escalation for a timed-out query"""
        if query_id not in self.pending_queries:
            return {"error": f"Query {query_id} not found"}
        
        query_data = self.pending_queries[query_id]
        elapsed_time = time.time() - query_data["timestamp"]
        
        escalation_message = f"""
TIMEOUT ESCALATION:
- Query: "{query_data['text']}"
- User: {query_data['user_id']}
- Elapsed: {elapsed_time/60:.1f} minutes
- Priority: {query_data['priority']}

REQUIRED ACTIONS:
1. Analyze why user hasn't responded
2. Check user context/activity if available
3. Suggest appropriate proactive response
4. Recommend next steps

Provide escalation strategy now.
"""
        
        response = self.process_message(escalation_message)
        self.system_state["successful_escalations"] += 1
        
        print(f"🚨 Escalation completed for query: {query_id}")
        return {
            "query_id": query_id,
            "escalation_response": response.get("response"),
            "success": True
        }
    
    def process_periodic_check(self) -> Dict[str, Any]:
        """Process periodic system check (called by internal clock)"""
        print("🕐 Orchestrator: Performing periodic check...")
        
        # Check for timeouts
        timed_out = self.check_timeouts()
        
        # Process escalations
        escalation_results = []
        for timeout_query in timed_out:
            result = self.initiate_escalation(timeout_query["id"])
            escalation_results.append(result)
        
        # Update system state
        self.system_state["last_periodic_check"] = time.time()
        
        return {
            "check_timestamp": time.time(),
            "timeouts_found": len(timed_out),
            "escalations": len(escalation_results),
            "system_health": "healthy" if len(timed_out) < 5 else "needs_attention"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "orchestrator": {
                "name": self.name,
                "agent_id": self.agent_id,
                "api_provider": "Gemini" if self.use_gemini else "Groq",
                "initialized": bool(self.agent_id)
            },
            "system_metrics": self.system_state,
            "active_queries": len(self.pending_queries),
            "active_workflows": len(self.active_workflows)
        }

# Test the updated orchestrator
if __name__ == "__main__":
    print("🧪 Testing Hybrid Orchestrator Agent...")
    
    orchestrator = OrchestratorAgent(use_gemini=True)
    
    if orchestrator.initialize():
        print("✅ Orchestrator initialized")
        
        # Test query tracking and escalation
        orchestrator.track_query("test_1", "What is your name?", "test_user")
        
        # Test immediate escalation (for testing)
        time.sleep(1)
        timeouts = orchestrator.check_timeouts(0)  # Immediate timeout
        
        if timeouts:
            print(f"✅ Found {len(timeouts)} timeouts")
            escalation = orchestrator.initiate_escalation(timeouts[0]["id"])
            print(f"Escalation response: {escalation.get('escalation_response', 'No response')[:100]}...")
        
        # Test periodic check
        periodic_result = orchestrator.process_periodic_check()
        print(f"✅ Periodic check: {periodic_result['system_health']}")
        
        print("🎉 Orchestrator test complete!")
    else:
        print("❌ Orchestrator initialization failed")
