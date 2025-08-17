"""
AI Life Agent Network - Centralized agent coordination and management
"""

from agents.orchestrator_agent import OrchestratorAgent
from typing import Dict, Any , List
import time

class AILifeAgentNetwork:
    """Centralized coordination of all AI agents in the system"""
    
    def __init__(self):
        """Initialize the agent network"""
        self.orchestrator = None
        self.agents = {}
        self.network_initialized = False
        self.initialization_time = None
        
        print("🌐 AI Life Agent Network created")

    def initialize_network(self) -> bool:
        """Initialize the complete agent network"""
        try:
            print("🚀 Initializing AI Life Agent Network...")
            
            # Step 1: Initialize the orchestrator agent
            self.orchestrator = OrchestratorAgent(use_gemini=True)
            
            if not self.orchestrator.initialize():
                print("❌ Orchestrator initialization failed")
                return False
            
            print("✅ Orchestrator initialized successfully")
            
            # Step 2: Get available agents from orchestrator
            self.agents = self._build_agent_registry()
            
            # Step 3: Verify network connectivity
            if not self._verify_network_health():
                print("⚠️ Network health check failed, but continuing...")
            
            self.network_initialized = True
            self.initialization_time = time.time()
            
            print(f"✅ Agent Network initialized with {len(self.agents)} agents")
            return True
            
        except Exception as e:
            print(f"❌ Agent Network initialization failed: {e}")
            return False

    def _build_agent_registry(self) -> Dict[str, Dict[str, Any]]:
        """Build registry of available agents from orchestrator"""
        agents_registry = {}
        
        try:
            if self.orchestrator and hasattr(self.orchestrator, 'available_agents'):
                for agent_name, agent_data in self.orchestrator.available_agents.items():
                    agents_registry[agent_name.lower()] = {
                        'id': agent_data.get('id'),
                        'name': agent_name,
                        'instance': agent_data.get('instance'),
                        'active': agent_data.get('active', True),
                        'registered_time': time.time()
                    }
                    
            print(f"📋 Built registry with {len(agents_registry)} agents")
            
        except Exception as e:
            print(f"⚠️ Failed to build agent registry: {e}")
            
        return agents_registry

    def _verify_network_health(self) -> bool:
        """Verify all agents are responding"""
        try:
            # Test orchestrator
            if not self.orchestrator or not self.orchestrator.agent_id:
                return False
                
            # Test that we have some agents available
            if len(self.agents) == 0:
                print("⚠️ No agents available in network")
                return False
                
            print("✅ Network health check passed")
            return True
            
        except Exception as e:
            print(f"⚠️ Network health check failed: {e}")
            return False

    def route_message(self, message: str) -> Dict[str, Any]:
        """Route message through the network (fallback method)"""
        if not self.network_initialized or not self.orchestrator:
            return {
                "response": "Agent network not initialized. Please restart the system.",
                "success": False,
                "error": "Network not initialized"
            }
            
        try:
            # Use orchestrator for routing
            routing_result = self.orchestrator.route_message(message)
            
            # Convert orchestrator response to expected format
            return {
                "response": routing_result.get('agent_response', routing_result.get('response', '')),
                "success": routing_result.get('routing_success', False),
                "routed_to": routing_result.get('routed_to', 'unknown'),
                "reasoning": routing_result.get('reasoning', ''),
                "response_time": routing_result.get('response_time', 0)
            }
            
        except Exception as e:
            print(f"❌ Network routing failed: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request.",
                "success": False,
                "error": str(e)
            }

    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status"""
        try:
            status = {
                "network_initialized": self.network_initialized,
                "initialization_time": self.initialization_time,
                "network_size": len(self.agents),
                "orchestrator_active": bool(self.orchestrator and self.orchestrator.agent_id),
                "available_agents": list(self.agents.keys()),
                "network_health": "healthy" if self.network_initialized else "offline"
            }
            
            # Get orchestrator metrics if available
            if self.orchestrator:
                orchestrator_status = self.orchestrator.get_system_status()
                status.update({
                    "routing_success_rate": orchestrator_status.get("routing_success_rate", 0),
                    "total_routes": orchestrator_status.get("system_metrics", {}).get("total_routes", 0)
                })
            
            return status
            
        except Exception as e:
            return {
                "network_initialized": False,
                "error": str(e),
                "network_health": "error"
            }

    def get_agent_by_name(self, agent_name: str) -> Dict[str, Any]:
        """Get specific agent information"""
        agent_key = agent_name.lower()
        return self.agents.get(agent_key, {})

    def is_agent_available(self, agent_name: str) -> bool:
        """Check if specific agent is available"""
        agent_data = self.get_agent_by_name(agent_name)
        return agent_data.get('active', False)

    def get_agent_list(self) -> List[str]:
        """Get list of available agent names"""
        return [agent_data.get('name', '') for agent_data in self.agents.values()]

    def shutdown_network(self):
        """Gracefully shutdown the agent network"""
        try:
            print("🛑 Shutting down Agent Network...")
            
            # Clear agents
            self.agents.clear()
            
            # Note: We don't shutdown orchestrator as it might be used elsewhere
            self.orchestrator = None
            
            self.network_initialized = False
            print("✅ Agent Network shutdown complete")
            
        except Exception as e:
            print(f"⚠️ Network shutdown error: {e}")

    def restart_network(self) -> bool:
        """Restart the agent network"""
        try:
            print("🔄 Restarting Agent Network...")
            self.shutdown_network()
            return self.initialize_network()
            
        except Exception as e:
            print(f"❌ Network restart failed: {e}")
            return False

# Test the agent network
if __name__ == "__main__":
    print("🧪 Testing AI Life Agent Network...")
    
    # Create and initialize network
    agent_network = AILifeAgentNetwork()
    
    if agent_network.initialize_network():
        print("✅ Network initialization successful")
        
        # Test network status
        status = agent_network.get_network_status()
        print(f"📊 Network Status: {status.get('network_health')} with {status.get('network_size')} agents")
        
        # Test message routing
        test_message = "I'm feeling stressed about work"
        result = agent_network.route_message(test_message)
        print(f"✅ Test routing: {result.get('success')} - routed to {result.get('routed_to')}")
        
        # Show available agents
        agents = agent_network.get_agent_list()
        print(f"📋 Available agents: {agents}")
        
        print("🎉 Agent Network test complete!")
        
    else:
        print("❌ Network initialization failed")
