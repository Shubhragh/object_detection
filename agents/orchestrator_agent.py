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

When routing messages, analyze user intent and select the BEST SPECIALIZED AGENT:

AVAILABLE AGENTS:
1. **ContextAgent**: Environmental context analysis, emotional state recognition, situational awareness
   - Use for: Emotional analysis, situation assessment, context interpretation, mood detection
   - Keywords: "feeling", "situation", "context", "environment", "mood", "state"

2. **CommunicationAgent**: Message crafting, relationship management, social intelligence
   - Use for: Relationship advice, communication help, social interactions, message writing
   - Keywords: "relationship", "talk", "communicate", "message", "social", "conversation"

3. **ProductivityAgent**: Time management, task organization, workflow efficiency
   - Use for: Time management, deadlines, task planning, organization, efficiency
   - Keywords: "time", "deadline", "organize", "productivity", "schedule", "manage", "task"

4. **StressManagementAgent**: Stress detection, coping strategies, emotional wellness
   - Use for: Stress relief, anxiety help, coping strategies, emotional support, overwhelm
   - Keywords: "stress", "overwhelmed", "anxiety", "pressure", "cope", "calm", "relax"

ROUTING DECISION FORMAT:
**Best Agent:** [agent_name]
**Explanation:** [Brief reason why this agent is most suitable]

When a user doesn't respond to a query within 2-5 minutes, initiate proactive escalation by consulting other agents for context.

Key Behaviors:
1. PROACTIVE: Always think ahead and prepare next steps
2. ROUTING: Direct tasks to the most appropriate specialized agent based on content and intent
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
        self.agent_registry = {}  # Will store available agents
        self.escalation_policies = {}
        self.system_state = {
            "active_conversations": 0,
            "total_queries_processed": 0,
            "successful_escalations": 0,
            "successful_routes": 0,
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
    
    def register_agent(self, agent_name: str, agent_data: Dict[str, Any]):
        """Register an agent with the orchestrator for routing"""
        self.agent_registry[agent_name.lower()] = agent_data
        print(f"📋 Registered agent: {agent_name}")
    
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
    
    def route_message(self, message: str, target_agent: str = None) -> Dict[str, Any]:
        """Enhanced routing with specialized agent selection"""
        
        # Update system metrics
        self.system_state["total_queries_processed"] += 1
        
        # Direct routing if target agent specified
        if target_agent and target_agent.lower() in self.agent_registry:
            agent_data = self.agent_registry[target_agent.lower()]
            response = self.hybrid_manager.send_message(agent_data['id'], message)
            self.system_state["successful_routes"] += 1
            return response
        
        # Smart routing - ask orchestrator to decide
        routing_message = f"""
ROUTING REQUEST:
User message: "{message}"

Available specialized agents in our system:
- ContextAgent: Environmental context analysis, emotional state recognition, situational awareness
- CommunicationAgent: Message crafting, relationship management, social intelligence  
- ProductivityAgent: Time management, task organization, workflow efficiency
- StressManagementAgent: Stress detection, coping strategies, emotional wellness

Based on the user's message content and intent, which agent should handle this request?

Respond with:
**Best Agent:** [exact agent name]
**Explanation:** [brief reason]
"""
        
        routing_response = self.process_message(routing_message)
        
        # Extract agent name from response
        response_text = routing_response.get('response', '')
        selected_agent = self._extract_agent_from_response(response_text)
        
        if selected_agent and selected_agent.lower() in self.agent_registry:
            # Route to selected agent
            agent_data = self.agent_registry[selected_agent.lower()]
            final_response = self.hybrid_manager.send_message(agent_data['id'], message)
            self.system_state["successful_routes"] += 1
            
            # Return routing decision + agent response
            return {
                "response": response_text,  # Include routing explanation
                "routed_to": selected_agent,
                "agent_response": final_response.get('response', ''),
                "routing_success": True
            }
        else:
            # Fallback - return orchestrator's routing analysis
            return {
                "response": response_text,
                "routed_to": "orchestrator",
                "routing_success": False,
                "note": "Could not identify suitable agent, provided analysis instead"
            }
    
    def _extract_agent_from_response(self, response_text: str) -> str:
        """Extract agent name from orchestrator's routing response"""
        import re
        
        # Look for patterns like "**Best Agent:** AgentName"
        patterns = [
            r'\*\*Best Agent:\*\*\s*`?([A-Za-z]+Agent)`?',
            r'\*\*Best Agent:\*\*\s*([A-Za-z]+Agent)',
            r'Best Agent:\s*`?([A-Za-z]+Agent)`?',
            r'Route to:\s*`?([A-Za-z]+Agent)`?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                agent_name = match.group(1)
                # Standardize agent names
                if 'context' in agent_name.lower():
                    return 'ContextAgent'
                elif 'communication' in agent_name.lower():
                    return 'CommunicationAgent'
                elif 'productivity' in agent_name.lower():
                    return 'ProductivityAgent'
                elif 'stress' in agent_name.lower():
                    return 'StressManagementAgent'
                else:
                    return agent_name
        
        # Fallback - analyze content for keywords
        message_lower = response_text.lower()
        if any(word in message_lower for word in ['stress', 'anxiety', 'overwhelm', 'pressure']):
            return 'StressManagementAgent'
        elif any(word in message_lower for word in ['time', 'deadline', 'productivity', 'organize']):
            return 'ProductivityAgent'
        elif any(word in message_lower for word in ['communication', 'relationship', 'social']):
            return 'CommunicationAgent'
        elif any(word in message_lower for word in ['context', 'situation', 'emotion', 'feeling']):
            return 'ContextAgent'
        
        return None
    
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
TIMEOUT ESCALATION ANALYSIS:
- Query: "{query_data['text']}"
- User: {query_data['user_id']}
- Elapsed: {elapsed_time/60:.1f} minutes
- Priority: {query_data['priority']}

REQUIRED ACTIONS:
1. Analyze why user hasn't responded (busy, away, distracted, unclear response needed)
2. Suggest appropriate proactive follow-up strategy
3. Recommend which specialized agent could provide additional context
4. Provide specific next steps for re-engagement

Generate proactive escalation strategy now.
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
        
        # Calculate system health
        total_queries = self.system_state["total_queries_processed"]
        success_rate = (self.system_state["successful_routes"] / max(1, total_queries)) * 100
        
        if success_rate > 90:
            health = "excellent"
        elif success_rate > 80:
            health = "healthy"
        elif len(timed_out) < 3:
            health = "healthy" 
        else:
            health = "needs_attention"
        
        return {
            "check_timestamp": time.time(),
            "timeouts_found": len(timed_out),
            "escalations": len(escalation_results),
            "system_health": health,
            "success_rate": f"{success_rate:.1f}%",
            "registered_agents": len(self.agent_registry)
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
            "active_workflows": len(self.active_workflows),
            "registered_agents": list(self.agent_registry.keys()),
            "routing_success_rate": (
                self.system_state["successful_routes"] / 
                max(1, self.system_state["total_queries_processed"])
            ) * 100
        }
    
    def get_routing_analytics(self) -> Dict[str, Any]:
        """Get routing performance analytics"""
        total_queries = self.system_state["total_queries_processed"]
        successful_routes = self.system_state["successful_routes"]
        
        return {
            "total_routing_requests": total_queries,
            "successful_routes": successful_routes,
            "routing_success_rate": f"{(successful_routes/max(1, total_queries))*100:.1f}%",
            "available_agents": list(self.agent_registry.keys()),
            "system_health": "optimal" if successful_routes/max(1, total_queries) > 0.9 else "good"
        }

# Test the enhanced orchestrator
if __name__ == "__main__":
    print("🧪 Testing Enhanced Hybrid Orchestrator Agent...")
    
    orchestrator = OrchestratorAgent(use_gemini=True)
    
    if orchestrator.initialize():
        print("✅ Enhanced Orchestrator initialized")
        
        # Test agent registration (simulate agent network setup)
        orchestrator.register_agent("ContextAgent", {"id": "test_context_001"})
        orchestrator.register_agent("StressManagementAgent", {"id": "test_stress_001"})
        
        # Test routing
        test_messages = [
            "I'm feeling stressed about work deadlines",
            "How can I better organize my daily tasks?",
            "I need help with a difficult conversation with my boss"
        ]
        
        for msg in test_messages:
            print(f"\n💬 Testing route: '{msg[:40]}...'")
            result = orchestrator.route_message(msg)
            print(f"✅ Routed to: {result.get('routed_to', 'unknown')}")
            print(f"Reasoning: {result.get('response', 'No response')[:100]}...")
        
        # Test query tracking and escalation
        orchestrator.track_query("test_1", "What is your name?", "test_user")
        
        # Test immediate escalation (for testing)
        time.sleep(1)
        timeouts = orchestrator.check_timeouts(0)  # Immediate timeout
        
        if timeouts:
            print(f"\n✅ Found {len(timeouts)} timeouts")
            escalation = orchestrator.initiate_escalation(timeouts[0]["id"])
            print(f"Escalation response: {escalation.get('escalation_response', 'No response')[:100]}...")
        
        # Test periodic check
        periodic_result = orchestrator.process_periodic_check()
        print(f"\n✅ Periodic check: {periodic_result['system_health']} ({periodic_result.get('success_rate', 'N/A')})")
        
        # Test system status
        status = orchestrator.get_system_status()
        print(f"✅ System status: {len(status['registered_agents'])} agents registered")
        
        # Test routing analytics
        analytics = orchestrator.get_routing_analytics()
        print(f"✅ Routing analytics: {analytics['routing_success_rate']} success rate")
        
        print("\n🎉 Enhanced Orchestrator test complete!")
    else:
        print("❌ Orchestrator initialization failed")
