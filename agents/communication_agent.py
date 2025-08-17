"""
Communication Optimization Agent for AI Life Operating System
Specialized in communication effectiveness and relationship management
"""

from agents.base_agent import BaseAgent
from hybrid_agent_manager import HybridAgentManager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_agent_manager import HybridAgentManager
from typing import List, Dict, Any
import time
import json

class CommunicationOptimizationAgent(BaseAgent):
    """Agent specialized in communication and relationships"""
    
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        super().__init__(
            name="CommunicationOptimizationAgent",
            specialization="Communication Effectiveness and Relationship Management",
            capabilities=[
                "Communication style analysis",
                "Message crafting optimization",
                "Relationship dynamics understanding",
                "Conflict resolution strategies"
            ],
            use_gemini=False,  # Use Groq for communication tasks
            hybrid_manager=hybrid_manager
        )
    
    def _generate_specialized_prompt(self) -> str:
        return f"""You are {self.name}, an expert in communication effectiveness and relationship management.

Your expertise includes:
• Analyzing and improving communication styles
• Crafting clear, effective messages
• Understanding relationship dynamics
• Resolving conflicts and misunderstandings

When helping with communication:
1. Analyze the communication context and goals
2. Identify communication strengths and areas for improvement
3. Suggest specific phrasing and approaches
4. Consider relationship dynamics and emotional factors
5. Provide conflict resolution strategies when needed

Always focus on empathy, clarity, and relationship building."""

    def improve_communication(self, communication_challenge: str) -> Dict[str, Any]:
        """Specialized method for communication improvement"""
        task = {
            "message": f"Provide communication improvement strategies for: '{communication_challenge}'"
        }
        return self.process_task(task)

# Test communication agent  
if __name__ == "__main__":
    print("🧪 Testing Communication Optimization Agent...")
    
    agent = CommunicationOptimizationAgent()
    if agent.initialize():
        result = agent.improve_communication("difficult conversation with my boss about workload")
        print(f"Communication Advice: {result.get('response', 'No response')[:100]}...")
    
    print("✅ Communication Optimization Agent test complete!")
