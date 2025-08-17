"""
Agents package initialization
"""

from .base_agent import BaseAgent
from .communication_agent import CommunicationOptimizationAgent
from .context_agent import ContextAnalysisAgent
from .emotional_analysis_agent import EmotionalAnalysisAgent
from .intent_classification_agent import IntentClassificationAgent
from .orchestrator_agent import OrchestratorAgent
from .productivity_agent import ProductivityAgent
from .stress_agent import StressManagementAgent

# Try to import ResponseHumanizerAgent if it exists
try:
    from .response_humanizer_agent import ResponseHumanizerAgent
except ImportError:
    print("⚠️ ResponseHumanizerAgent not found - responses will be less natural")
    ResponseHumanizerAgent = None

__all__ = [
    'BaseAgent',
    'CommunicationOptimizationAgent', 
    'ContextAnalysisAgent',
    'EmotionalAnalysisAgent',
    'IntentClassificationAgent',
    'OrchestratorAgent',
    'ProductivityAgent',
    'StressManagementAgent',
    'ResponseHumanizerAgent'
]
