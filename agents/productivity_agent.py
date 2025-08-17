"""
Productivity Agent for AI Life Operating System
Specialized in productivity enhancement and time management
"""

from agents.base_agent import BaseSpecializedAgent
from hybrid_agent_manager import HybridAgentManager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_agent_manager import HybridAgentManager
from typing import List, Dict, Any
import time
import json

class ProductivityAgent(BaseSpecializedAgent):
    """Agent specialized in productivity and time management"""
    
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        super().__init__(
            name="ProductivityAgent",
            specialization="Productivity Enhancement and Time Management",
            capabilities=[
                "Time allocation optimization",
                "Task prioritization strategies",
                "Workflow efficiency analysis",
                "Goal achievement planning"
            ],
            use_gemini=False,  # Use Groq for productivity tasks
            hybrid_manager=hybrid_manager
        )
    
    def _generate_specialized_prompt(self) -> str:
        return f"""You are {self.name}, an expert in productivity optimization and time management.

Your expertise includes:
• Analyzing and optimizing time allocation
• Creating effective task prioritization systems
• Designing efficient workflows
• Setting and achieving goals systematically

When helping with productivity:
1. Assess current productivity challenges
2. Identify time wasters and inefficiencies  
3. Recommend specific productivity techniques (Pomodoro, GTD, etc.)
4. Create actionable task organization systems
5. Provide goal-setting and tracking strategies

Always provide practical, immediately actionable advice."""

    def optimize_workflow(self, productivity_challenge: str) -> Dict[str, Any]:
        """Specialized method for workflow optimization"""
        task = {
            "message": f"Analyze and provide workflow optimization strategies for: '{productivity_challenge}'"
        }
        return self.process_task(task)

# Test productivity agent
if __name__ == "__main__":
    print("🧪 Testing Productivity Agent...")
    
    agent = ProductivityAgent()
    if agent.initialize():
        result = agent.optimize_workflow("managing multiple projects with tight deadlines")
        print(f"Productivity Tips: {result.get('response', 'No response')[:100]}...")
    
    print("✅ Productivity Agent test complete!")
