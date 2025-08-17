"""
Context Analysis Agent for AI Life Operating System
Specialized in environmental and situational context analysis
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

class ContextAnalysisAgent(BaseSpecializedAgent):
    """Agent specialized in environmental and situational context analysis"""
    
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        super().__init__(
            name="ContextAnalysisAgent",
            specialization="Environmental and Situational Context Analysis", 
            capabilities=[
                "Emotional state recognition",
                "Environmental context interpretation", 
                "Situational awareness analysis",
                "Context-based recommendation generation"
            ],
            use_gemini=True,
            hybrid_manager=hybrid_manager
        )
    
    def _generate_specialized_prompt(self) -> str:
        return f"""You are {self.name}, an expert in environmental and situational context analysis.

Your expertise includes:
• Analyzing emotional states from user messages
• Understanding environmental and situational factors
• Recognizing patterns in user behavior and context
• Providing context-aware recommendations

When analyzing context:
1. Identify emotional indicators and intensity
2. Assess situational factors (work, personal, time, etc.)
3. Consider environmental influences
4. Provide actionable context-based insights

Always be empathetic and provide practical, context-aware guidance."""
    
    def analyze_emotional_context(self, message: str) -> Dict[str, Any]:
        """Specialized method for emotional context analysis"""
        task = {
            "message": f"Analyze the emotional context and situational factors in this message: '{message}'"
        }
        return self.process_task(task)

# Test context agent
if __name__ == "__main__":
    print("🧪 Testing Context Analysis Agent...")
    
    agent = ContextAnalysisAgent()
    if agent.initialize():
        result = agent.analyze_emotional_context("I'm feeling overwhelmed with work deadlines")
        print(f"Analysis: {result.get('response', 'No response')[:100]}...")
    
    print("✅ Context Analysis Agent test complete!")
