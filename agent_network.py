from hybrid_agent_manager import HybridAgentManager
from agents.orchestrator_agent import OrchestratorAgent
from typing import Dict, Any, List
import time


class AILifeAgentNetwork:
    def __init__(self):
        self.hybrid_manager = HybridAgentManager()
        self.agents = {}
        self.orchestrator = None
    
    def initialize_network(self):
        """Initialize all agents in the network"""
        print("🚀 Initializing AI Life Agent Network...")
        
        # 1. Initialize Orchestrator
        self.orchestrator = OrchestratorAgent(use_gemini=True)
        if self.orchestrator.initialize():
            self.agents["orchestrator"] = self.orchestrator
            print("✅ Orchestrator ready")
        else:
            print("❌ Failed to initialize Orchestrator")
            return False
        
        # 2. Create specialized agents
        agent_configs = [
            # Your existing agents
            {
                "name": "ContextAgent", 
                "role": "Environmental context analysis and activity recognition",
                "use_gemini": True
            },
            {
                "name": "CommunicationAgent",
                "role": "Message crafting, relationship management, and social intelligence",
                "use_gemini": False
            },
            # NEW SPECIALIZED AGENTS
            {
                "name": "StressManagementAgent",
                "role": "Stress detection, coping strategies, and emotional wellness support with evidence-based techniques",
                "use_gemini": True
            },
            {
                "name": "ProductivityAgent", 
                "role": "Time management optimization, task prioritization, and workflow efficiency enhancement",
                "use_gemini": False
            }
        ]
        
        # 3. Create all specialized agents
        for config in agent_configs:
            agent = self._create_specialized_agent(
                config["name"],
                config["role"], 
                config["use_gemini"]
            )
            if agent:
                self.agents[config["name"].lower()] = agent
                print(f"✅ {config['name']} ready")
            else:
                print(f"❌ Failed to create {config['name']}")
        
        # 4. Register agents with orchestrator for smart routing
        if self.orchestrator and len(self.agents) > 1:
            registered_count = 0
            for agent_name, agent_data in self.agents.items():
                if agent_name != 'orchestrator':  # Don't register orchestrator with itself
                    try:
                        self.orchestrator.register_agent(agent_name, agent_data)
                        registered_count += 1
                    except Exception as e:
                        print(f"⚠️ Failed to register {agent_name}: {e}")
            
            print(f"✅ Registered {registered_count} agents with orchestrator")
        
        print(f"🎉 Network initialized with {len(self.agents)} agents")
        return len(self.agents) > 1
    
    def _create_specialized_agent(self, name: str, role: str, use_gemini: bool):
        """Create a specialized agent with role-specific prompt"""
        system_prompt = f"""You are {name}, a specialized agent in a proactive multi-agent AI system.

Your role: {role}

Core capabilities:
- Analyze requests within your domain expertise
- Provide actionable insights and recommendations
- Collaborate with other agents when needed
- Maintain proactive rather than reactive behavior
- Keep responses focused and practical

When you receive a request:
1. Determine if it's within your expertise
2. Provide specific, actionable advice
3. Suggest next steps or additional resources
4. Alert if other agents should be involved

You are part of a living AI system that never waits passively."""
        
        try:
            agent_data = self.hybrid_manager.create_agent(name, system_prompt, use_gemini)
            
            if agent_data and agent_data.get('id'):
                return {
                    "id": agent_data['id'],
                    "name": name,
                    "role": role,
                    "use_gemini": use_gemini,
                    "hybrid_manager": self.hybrid_manager
                }
        except Exception as e:
            print(f"❌ Error creating {name}: {e}")
        
        return None

    def route_message(self, message: str, target_agent: str = None) -> Dict[str, Any]:
        """Route message to appropriate agent"""
        if target_agent and target_agent.lower() in self.agents:
            # Direct routing
            agent = self.agents[target_agent.lower()]
            try:
                if hasattr(agent, 'process_message'):
                    return agent.process_message(message)
                else:
                    return self.hybrid_manager.send_message(agent['id'], message)
            except Exception as e:
                return {"error": f"Failed to send message to {target_agent}: {e}"}
        else:
            # Route through orchestrator for decision
            if self.orchestrator:
                routing_message = f"""
ROUTING REQUEST:
User message: "{message}"
Available agents: {list(self.agents.keys())}

Determine the best agent to handle this request and explain why.
If multiple agents needed, suggest coordination approach.
"""
                try:
                    return self.orchestrator.process_message(routing_message)
                except Exception as e:
                    return {"error": f"Orchestrator routing failed: {e}"}
        
        return {"error": "No suitable agent found or orchestrator unavailable"}
    
    def broadcast_message(self, message: str) -> Dict[str, Any]:
        """Send message to all agents for collective input"""
        responses = {}
        
        for agent_name, agent in self.agents.items():
            try:
                if hasattr(agent, 'process_message'):
                    response = agent.process_message(message)
                else:
                    response = self.hybrid_manager.send_message(agent['id'], message)
                
                responses[agent_name] = response.get('response', 'No response')
            except Exception as e:
                responses[agent_name] = f"Error: {e}"
        
        return responses
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get status of entire agent network"""
        agent_statuses = {}
        
        for agent_name, agent in self.agents.items():
            try:
                if hasattr(agent, 'get_system_status'):
                    agent_statuses[agent_name] = agent.get_system_status()
                else:
                    agent_statuses[agent_name] = {
                        "name": agent.get('name', agent_name),
                        "id": agent.get('id', 'unknown'),
                        "role": agent.get('role', 'Unknown role'),
                        "use_gemini": agent.get('use_gemini', False),
                        "active": True
                    }
            except Exception as e:
                agent_statuses[agent_name] = {
                    "name": agent_name,
                    "active": False,
                    "error": str(e)
                }
        
        return {
            "network_size": len(self.agents),
            "agents": agent_statuses,
            "orchestrator_active": self.orchestrator is not None,
            "timestamp": time.time()
        }
    
    def send_direct_message(self, agent_name: str, message: str) -> Dict[str, Any]:
        """Send message directly to a specific agent"""
        agent_name = agent_name.lower()
        
        if agent_name not in self.agents:
            return {"error": f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}"}
        
        return self.route_message(message, agent_name)
    
    def get_agent_capabilities(self) -> Dict[str, str]:
        """Get a summary of all agent capabilities"""
        capabilities = {}
        
        for agent_name, agent_data in self.agents.items():
            if isinstance(agent_data, dict) and 'role' in agent_data:
                capabilities[agent_name] = agent_data['role']
            elif hasattr(agent_data, 'role'):
                capabilities[agent_name] = agent_data.role
            else:
                capabilities[agent_name] = "General AI assistant"
        
        return capabilities
    
    def shutdown_network(self):
        """Gracefully shutdown all agents"""
        print("🔄 Shutting down AI Life Agent Network...")
        
        shutdown_count = 0
        for agent_name, agent in self.agents.items():
            try:
                if hasattr(agent, 'shutdown'):
                    agent.shutdown()
                elif isinstance(agent, dict) and 'id' in agent:
                    # Attempt to cleanup via hybrid manager
                    self.hybrid_manager.cleanup_agent(agent['id'])
                shutdown_count += 1
                print(f"✅ {agent_name} shut down")
            except Exception as e:
                print(f"⚠️ Error shutting down {agent_name}: {e}")
        
        self.agents.clear()
        self.orchestrator = None
        print(f"🏁 Network shutdown complete. {shutdown_count} agents stopped.")


# Test the complete network
if __name__ == "__main__":
    print("🧪 Testing Complete AI Life Agent Network...")
    
    network = AILifeAgentNetwork()
    
    if network.initialize_network():
        print("✅ Network initialization successful")
        
        # Display agent capabilities
        print("\n📋 Agent Capabilities:")
        capabilities = network.get_agent_capabilities()
        for agent_name, role in capabilities.items():
            print(f"  🤖 {agent_name}: {role}")
        
        # Test routing
        print("\n🧪 Testing message routing...")
        test_message = "I feel stressed and need help managing my time"
        response = network.route_message(test_message)
        print(f"Routing response: {response.get('response', 'No response')[:200]}...")
        
        # Test direct agent communication
        print("\n🧪 Testing direct agent communication...")
        if 'contextagent' in network.agents:
            context_response = network.send_direct_message(
                "contextagent",
                "Analyze my current environment and suggest optimizations"
            )
            print(f"Context agent: {context_response.get('response', 'No response')[:100]}...")
        
        # Test broadcast
        print("\n🧪 Testing broadcast message...")
        broadcast_responses = network.broadcast_message("What's the most important thing I should focus on today?")
        print(f"Received {len(broadcast_responses)} responses from broadcast")
        
        # Test network status
        print("\n📊 Network Status:")
        status = network.get_network_status()
        print(f"Active agents: {status['network_size']}")
        for agent_name, agent_info in status['agents'].items():
            status_icon = "✅" if agent_info.get('active', False) else "❌"
            print(f"  {status_icon} {agent_name}: {agent_info.get('role', 'Unknown role')[:50]}...")
        
        # Graceful shutdown
        print("\n🔄 Testing graceful shutdown...")
        network.shutdown_network()
        
        print("\n🎉 Complete network test successful!")
    else:
        print("❌ Network initialization failed")
