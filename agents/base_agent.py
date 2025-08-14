from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from letta_manager import LettaManager

class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.letta = LettaManager()
        self.agent_id = None
        self.memory_state = {}
        
    def initialize(self) -> bool:
        """Initialize the agent in Letta"""
        agent_data = self.letta.create_agent(
            name=self.name,
            system_prompt=self.system_prompt,
            tools=self.get_tools()
        )
        
        if agent_data:
            self.agent_id = agent_data.get('id')
            print(f"✅ {self.name} initialized with ID: {self.agent_id}")
            return True
        return False
    
    @abstractmethod
    def get_tools(self) -> List[str]:
        """Return list of tools this agent needs"""
        pass
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """Process a message through the agent"""
        if not self.agent_id:
            return {"error": "Agent not initialized"}
        
        response = self.letta.send_message(self.agent_id, message)
        self.update_memory_state()
        return response
    
    def update_memory_state(self):
        """Update local memory state from Letta"""
        if self.agent_id:
            self.memory_state = self.letta.get_agent_memory(self.agent_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and memory"""
        return {
            "name": self.name,
            "agent_id": self.agent_id,
            "memory_state": self.memory_state,
            "initialized": bool(self.agent_id)
        }
