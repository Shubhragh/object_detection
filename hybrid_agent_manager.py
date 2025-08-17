"""
CORRECTED Hybrid Agent Manager - Fixed send_message response handling
"""

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
        """CORRECTED: Send message with proper success/failure handling"""
        
        # Check if agent exists
        if agent_id not in self.active_agents:
            return {
                "success": False,
                "error": "Agent not found",
                "agent_id": agent_id
            }

        # Validate message
        if not message or not message.strip():
            return {
                "success": False,
                "error": "Empty message",
                "agent_id": agent_id
            }

        agent_info = self.active_agents[agent_id]

        try:
            # Build context from conversation history
            context = f"You are {agent_info['name']}. {agent_info['system_prompt']}\n\n"

            # Add recent conversation history for context
            recent_history = agent_info['conversation_history'][-5:]  # Last 5 exchanges
            for exchange in recent_history:
                context += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n\n"

            context += f"User: {message}\nAssistant:"

            # Generate response directly via API
            response_text = self.api_manager.generate_response(
                context,
                use_gemini=agent_info['use_gemini']
            )

            # Check if response is valid
            if not response_text or response_text.startswith("Error:"):
                return {
                    "success": False,
                    "error": f"API generation failed: {response_text}",
                    "agent_id": agent_id
                }

            # Store in conversation history
            agent_info['conversation_history'].append({
                "user": message,
                "assistant": response_text,
                "timestamp": time.time()
            })

            # Return successful response
            return {
                "success": True,
                "response": response_text,
                "agent_id": agent_id,
                "agent_name": agent_info['name'],
                "source": "hybrid_direct"
            }

        except Exception as e:
            print(f"❌ Hybrid agent {agent_id} error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent_id
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

# Test the corrected hybrid manager
if __name__ == "__main__":
    import time

    print("🧪 Testing Corrected Hybrid Agent Manager")

    hybrid = HybridAgentManager()

    # Create test agent
    test_agent = hybrid.create_agent(
        "TestStressAgent",
        "You are a helpful stress management assistant. Provide empathetic, supportive responses to users experiencing stress or emotional difficulties.",
        use_gemini=True
    )

    if test_agent:
        print(f"✅ Created agent: {test_agent['id']}")
        
        # Test successful message
        response1 = hybrid.send_message(test_agent['id'], "I am feeling stressed out")
        print(f"✅ Response 1 success: {response1.get('success')}")
        if response1.get('success'):
            print(f"Response: {response1.get('response', '')[:100]}...")
        
        # Test invalid agent
        response2 = hybrid.send_message("invalid_id", "Hello")
        print(f"✅ Response 2 success: {response2.get('success')} (should be False)")
        
        # Test empty message
        response3 = hybrid.send_message(test_agent['id'], "")
        print(f"✅ Response 3 success: {response3.get('success')} (should be False)")
        
    else:
        print("❌ Failed to create test agent")
