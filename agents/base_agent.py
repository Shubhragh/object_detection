"""
Base Agent class for all specialized agents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_agent_manager import HybridAgentManager
from memory.memory_manager import MemoryManager
from typing import Dict, Any

class BaseAgent:
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        self.hybrid_manager = hybrid_manager or HybridAgentManager()
        self.memory_manager = MemoryManager()  # Direct memory access
        self.name = "BaseAgent"
        self.agent_id = None
        self.system_prompt = "Base agent prompt"

    def initialize(self) -> bool:
        """Initialize the agent"""
        agent_data = self.hybrid_manager.create_agent(
            self.name,
            self.system_prompt,
            use_gemini=True
        )

        if agent_data and agent_data.get('id'):
            self.agent_id = agent_data['id']
            print(f"✅ {self.name} initialized: {self.agent_id}")
            return True
        
        print(f"❌ {self.name} initialization failed")
        return False

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with memory context"""
        try:
            message = task.get('message', '')
            
            # Get user's memory context
            user_memories = self.memory_manager.retrieve_experiences("user", 5)
            memory_context = self._format_memory_context(user_memories)
            
            # Build context-aware prompt
            context_prompt = f"""
RECENT USER CONTEXT:
{memory_context}

CURRENT USER MESSAGE: "{message}"

Respond based on the user's history and current message. Be contextually aware.
"""

            response = self.hybrid_manager.send_message(self.agent_id, context_prompt)
            
            if response.get('success'):
                return {
                    "success": True,
                    "response": response.get('response', ''),
                    "memory_used": len(user_memories)
                }
            else:
                return {"success": False, "error": response.get('error', 'Unknown error')}

        except Exception as e:
            print(f"❌ {self.name} task processing failed: {e}")
            return {"success": False, "error": str(e)}

    def _format_memory_context(self, memories: list) -> str:
        """Format user memories for context"""
        if not memories:
            return "No previous interactions stored."
        
        context_lines = []
        for i, memory in enumerate(memories[:3]):  # Last 3 interactions
            exp_data = memory.get('experience', {})
            message = exp_data.get('message', 'N/A')
            timestamp = memory.get('timestamp', 'Unknown time')
            context_lines.append(f"{i+1}. {timestamp}: {message[:80]}...")
        
        return "\n".join(context_lines)
