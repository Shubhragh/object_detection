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
        
        # 2. Initialize specialized agents
        agent_configs = [
            {
                "name": "ContextAgent", 
                "role": "Environmental context analysis and activity recognition",
                "use_gemini": True
            },
            {
                "name": "MemoryCuratorAgent",
                "role": "Memory management, pattern recognition, and knowledge synthesis", 
                "use_gemini": True
            },
            {
                "name": "CommunicationAgent",
                "role": "Message crafting, relationship management, and social intelligence",
                "use_gemini": False  # Use Groq for communication
            },
            {
                "name": "LearningAgent",
                "role": "System improvement, outcome analysis, and adaptation",
                "use_gemini": False  # Use Groq for learning
            }
        ]
        
        for config in agent_configs:
            agent = self._create_specialized_agent(
                config["name"],
                config["role"], 
                config["use_gemini"]
            )
            if agent:
                self.agents[config["name"].lower()] = agent
                print(f"✅ {config['name']} ready")
        
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
        
        agent_data = self.hybrid_manager.create_agent(name, system_prompt, use_gemini)
        
        if agent_data and agent_data.get('id'):
            return {
                "id": agent_data['id'],
                "name": name,
                "role": role,
                "use_gemini": use_gemini,
                "hybrid_manager": self.hybrid_manager
            }
        return None
    
    def route_message(self, message: str, target_agent: str = None) -> Dict[str, Any]:
        """Route message to appropriate agent"""
        if target_agent and target_agent.lower() in self.agents:
            # Direct routing
            agent = self.agents[target_agent.lower()]
            if hasattr(agent, 'process_message'):
                return agent.process_message(message)
            else:
                return self.hybrid_manager.send_message(agent['id'], message)
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
                return self.orchestrator.process_message(routing_message)
        
        return {"error": "No suitable agent found"}
    
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
            if hasattr(agent, 'get_system_status'):
                agent_statuses[agent_name] = agent.get_system_status()
            else:
                agent_statuses[agent_name] = {
                    "name": agent.get('name', agent_name),
                    "id": agent.get('id', 'unknown'),
                    "active": True
                }
        
        return {
            "network_size": len(self.agents),
            "agents": agent_statuses,
            "orchestrator_active": self.orchestrator is not None
        }

# Test the complete network
if __name__ == "__main__":
    print("🧪 Testing Complete AI Life Agent Network...")
    
    network = AILifeAgentNetwork()
    
    if network.initialize_network():
        print("✅ Network initialization successful")
        
        # Test routing
        print("\n🧪 Testing message routing...")
        response = network.route_message("I feel stressed and need help managing my time")
        print(f"Routing response: {response.get('response', 'No response')[:150]}...")
        
        # Test direct agent communication
        print("\n🧪 Testing direct agent communication...")
        context_response = network.route_message(
            "Analyze my current environment and suggest optimizations",
            "contextagent"
        )
        print(f"Context agent: {context_response.get('response', 'No response')[:100]}...")
        
        # Test network status
        print("\n🧪 Network status:")
        status = network.get_network_status()
        print(f"Active agents: {status['network_size']}")
        for agent_name in status['agents'].keys():
            print(f"  - {agent_name}: ✅ Active")
        
        print("\n🎉 Complete network test successful!")
    else:
        print("❌ Network initialization failed")
