from letta_manager import LettaManager
from api_manager import APIManager
from typing import Dict, Any
import time
import json

class HybridAgentManager:
    def __init__(self):
        self.letta = LettaManager()
        self.api_manager = APIManager()
        self.active_agents = {}
    
    def create_agent(self, name: str, system_prompt: str, use_gemini: bool = True) -> Dict[str, Any]:
        """Create agent via Letta but store for direct communication"""
        
        # Create agent through Letta (this works)
        agent = self.letta.create_agent(name, system_prompt, use_gemini=use_gemini)
        
        if agent and agent.get('id'):
            # Store agent info for direct communication
            self.active_agents[agent['id']] = {
                "name": name,
                "system_prompt": system_prompt,
                "use_gemini": use_gemini,
                "letta_id": agent['id'],
                "conversation_history": []
            }
            
            print(f"✅ Hybrid agent created: {name} (ID: {agent['id']})")
            return agent
        
        return None
    
    def send_message(self, agent_id: str, message: str) -> Dict[str, Any]:
        """Send message directly via API, maintaining context"""
        
        if agent_id not in self.active_agents:
            return {"error": "Agent not found"}
        
        agent_info = self.active_agents[agent_id]
        
        # Build context from conversation history
        context = f"You are {agent_info['name']}. {agent_info['system_prompt']}\n\n"
        
        # Add recent conversation history for context
        recent_history = agent_info['conversation_history'][-5:]  # Last 5 exchanges
        for exchange in recent_history:
            context += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n\n"
        
        context += f"User: {message}\nAssistant:"
        
        # Generate response directly via API
        response = self.api_manager.generate_response(
            context,
            use_gemini=agent_info['use_gemini']
        )
        
        # Store in conversation history
        agent_info['conversation_history'].append({
            "user": message,
            "assistant": response,
            "timestamp": time.time()
        })
        
        print(f"✅ Hybrid response generated for {agent_id}")
        
        return {
            "agent_id": agent_id,
            "message": message,
            "response": response,
            "source": "hybrid_direct"
        }
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get agent status and conversation history"""
        if agent_id in self.active_agents:
            agent_info = self.active_agents[agent_id]
            return {
                "agent_id": agent_id,
                "name": agent_info['name'],
                "active": True,
                "conversation_count": len(agent_info['conversation_history']),
                "last_interaction": agent_info['conversation_history'][-1]['timestamp'] if agent_info['conversation_history'] else None
            }
        return {"agent_id": agent_id, "active": False}

# Test hybrid approach
if __name__ == "__main__":
    import time
    
    print("🧪 Testing Hybrid Agent Manager")
    
    hybrid = HybridAgentManager()
    
    # Create agents
    gemini_agent = hybrid.create_agent(
        "HybridGemini",
        "You are a helpful AI assistant using Gemini 2.5 Flash. Keep responses concise and helpful.",
        use_gemini=True
    )
    
    groq_agent = hybrid.create_agent(
        "HybridGroq", 
        "You are a helpful AI assistant using Llama 3.3 70B. Keep responses concise and helpful.",
        use_gemini=False
    )
    
    # Test messaging
    if gemini_agent:
        response1 = hybrid.send_message(
            gemini_agent['id'],
            "Hello! What's your name and which model are you using?"
        )
        print(f"Gemini: {response1['response']}")
        
        response2 = hybrid.send_message(
            gemini_agent['id'], 
            "Can you remember what I just asked you?"
        )
        print(f"Gemini Memory Test: {response2['response']}")
    
    if groq_agent:
        response = hybrid.send_message(
            groq_agent['id'],
            "Hello! What's your name and which model are you using?"
        )
        print(f"Groq: {response['response']}")
