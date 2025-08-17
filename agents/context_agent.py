"""
CORRECTED Context Agent with Memory Access
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from typing import Dict, Any

class ContextAnalysisAgent(BaseAgent):
    def __init__(self, hybrid_manager=None):
        super().__init__(hybrid_manager)
        self.name = "ContextAnalysisAgent"
        self.system_prompt = """You are a Context Analysis Agent who provides information, answers questions, and handles system queries.

When asked about stored experiences or memory:
- Access and summarize the user's interaction history
- Provide clear information about what's been stored
- Be factual about the system's memory capabilities

For general questions, provide helpful, accurate information.
Be conversational but informative."""

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Handle system queries with direct memory access"""
        try:
            message = task.get('message', '').lower()
            
            # Special handling for memory/experience queries
            if any(word in message for word in ['previous', 'experiences', 'stored', 'memory', 'remember', 'history']):
                return self._handle_memory_query(task)
            else:
                # Use parent method for general queries
                return super().process_task(task)

        except Exception as e:
            print(f"❌ ContextAgent memory query failed: {e}")
            return {"success": False, "error": str(e)}

    def _handle_memory_query(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle queries about stored memories"""
        try:
            # Get all user experiences
            user_memories = self.memory_manager.retrieve_experiences("user", 50)
            memory_stats = self.memory_manager.get_memory_statistics("user")
            
            if not user_memories:
                response = "I don't have any previous experiences or conversations stored for you yet. This might be our first interaction, or there could be an issue with memory storage."
            else:
                # Format memory summary
                recent_interactions = []
                for i, memory in enumerate(user_memories[:10]):
                    exp_data = memory.get('experience', {})
                    message = exp_data.get('message', 'N/A')
                    exp_type = exp_data.get('type', 'unknown')
                    timestamp = memory.get('timestamp', 'Unknown time')
                    importance = memory.get('importance', 0.5)
                    
                    recent_interactions.append(
                        f"{i+1}. [{timestamp}] Type: {exp_type}, Importance: {importance:.2f}\n   Message: \"{message[:100]}{'...' if len(message) > 100 else ''}\""
                    )

                response = f"""Here's what I have stored for you:

**Memory Statistics:**
- Total experiences: {memory_stats.get('total_experiences', 0)}
- Memory health: {memory_stats.get('memory_health', 'unknown')}
- Average importance: {memory_stats.get('average_importance', 0.0)}

**Recent Interactions (last 10):**
{chr(10).join(recent_interactions)}

The system stores your messages, responses, emotional context, and importance scores to provide better assistance over time."""

            return {
                "success": True,
                "response": response,
                "memory_count": len(user_memories)
            }

        except Exception as e:
            print(f"❌ Memory query processing failed: {e}")
            return {
                "success": True,
                "response": f"I encountered an error accessing your stored experiences: {str(e)}. The memory system might need attention."
            }
