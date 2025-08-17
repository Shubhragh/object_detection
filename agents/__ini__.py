"""
Specialized Agents Module for AI Life Operating System
"""

from .base_agent import BaseSpecializedAgent
from .context_agent import ContextAnalysisAgent
from .stress_agent import StressManagementAgent
from .productivity_agent import ProductivityAgent
from .communication_agent import CommunicationOptimizationAgent

__all__ = [
    'BaseSpecializedAgent',
    'ContextAnalysisAgent', 
    'StressManagementAgent',
    'ProductivityAgent',
    'LearningOptimizationAgent',
    'CommunicationOptimizationAgent',
    'AgentEcosystemManager'
]
