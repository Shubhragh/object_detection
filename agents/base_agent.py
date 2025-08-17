"""
Base Agent Class for AI Life Operating System
Foundation for all specialized agents
"""

from typing import Dict, Any, List, Optional
from hybrid_agent_manager import HybridAgentManager
import time

class BaseSpecializedAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, specialization: str, capabilities: List[str], 
                 use_gemini: bool = True, hybrid_manager: HybridAgentManager = None):
        self.name = name
        self.specialization = specialization
        self.capabilities = capabilities
        self.use_gemini = use_gemini
        self.hybrid_manager = hybrid_manager or HybridAgentManager()
        
        # Agent state
        self.agent_id = None
        self.initialized = False
        self.completed_tasks = 0
        self.success_rate = 1.0
        self.expertise_level = 0.5
        
        # Performance metrics
        self.performance_metrics = {
            "total_interactions": 0,
            "successful_responses": 0,
            "average_response_time": 0.0
        }
    
    def initialize(self) -> bool:
        """Initialize the specialized agent"""
        system_prompt = self._generate_specialized_prompt()
        agent_data = self.hybrid_manager.create_agent(self.name, system_prompt, self.use_gemini)
        
        if agent_data and 'id' in agent_data:
            self.agent_id = agent_data['id']
            self.initialized = True
            print(f"✅ {self.name} ({self.specialization}) initialized")
            return True
        return False
    
    def _generate_specialized_prompt(self) -> str:
        """Generate specialized system prompt - override in subclasses"""
        return f"""You are {self.name}, specialized in {self.specialization}.
        
Capabilities: {', '.join(self.capabilities)}
        
Provide expert assistance in your domain while collaborating effectively with other agents."""
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task through this agent"""
        if not self.initialized:
            return {"error": "Agent not initialized", "agent": self.name}
        
        start_time = time.time()
        
        try:
            response = self.hybrid_manager.send_message(
                self.agent_id, 
                task.get("message", ""), 
                use_gemini=self.use_gemini
            )
            
            response_time = time.time() - start_time
            self._update_metrics(True, response_time)
            
            return {
                "agent": self.name,
                "specialization": self.specialization,
                "response": response.get("response", "No response"),
                "response_time": response_time,
                "success": True
            }
            
        except Exception as e:
            self._update_metrics(False, 0)
            return {"agent": self.name, "error": str(e), "success": False}
    
    def _update_metrics(self, success: bool, response_time: float):
        """Update agent performance metrics"""
        self.performance_metrics["total_interactions"] += 1
        if success:
            self.performance_metrics["successful_responses"] += 1
        
        # Update success rate
        self.success_rate = (
            self.performance_metrics["successful_responses"] / 
            self.performance_metrics["total_interactions"]
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "specialization": self.specialization,
            "initialized": self.initialized,
            "success_rate": self.success_rate,
            "expertise_level": self.expertise_level,
            "total_interactions": self.performance_metrics["total_interactions"]
        }
