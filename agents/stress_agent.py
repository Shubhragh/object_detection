"""
Stress Management Agent for AI Life Operating System
Specialized in stress detection and management techniques
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

class StressManagementAgent(BaseSpecializedAgent):
    """Agent specialized in stress detection and management"""
    
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        super().__init__(
            name="StressManagementAgent",
            specialization="Stress Detection and Management",
            capabilities=[
                "Stress pattern recognition",
                "Coping strategy recommendation", 
                "Relaxation technique guidance",
                "Workload optimization advice"
            ],
            use_gemini=True,
            hybrid_manager=hybrid_manager
        )
    
    def _generate_specialized_prompt(self) -> str:
        return f"""You are {self.name}, an expert in stress management and emotional wellness.

Your expertise includes:
• Identifying stress patterns and triggers
• Recommending evidence-based coping strategies
• Teaching relaxation and mindfulness techniques
• Providing workload and time management advice

When helping with stress:
1. Validate the user's experience
2. Identify specific stress triggers
3. Suggest immediate relief techniques
4. Recommend long-term stress management strategies
5. Provide practical, actionable steps

Always be supportive, empathetic, and focus on evidence-based techniques."""

    def provide_stress_relief(self, stress_description: str) -> Dict[str, Any]:
        """Specialized method for stress relief recommendations"""
        task = {
            "message": f"Provide immediate stress relief techniques and long-term management strategies for: '{stress_description}'"
        }
        return self.process_task(task)

# Test stress agent
if __name__ == "__main__":
    print("🧪 Testing Stress Management Agent...")
    
    agent = StressManagementAgent()
    if agent.initialize():
        result = agent.provide_stress_relief("work deadline pressure and overwhelming tasks")
        print(f"Stress Relief: {result.get('response', 'No response')[:100]}...")
    
    print("✅ Stress Management Agent test complete!")
