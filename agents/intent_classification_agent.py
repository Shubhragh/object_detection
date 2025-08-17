"""
Intent Classification Agent for AI Life Operating System
Specialized in understanding user intent and message classification
"""

from hybrid_agent_manager import HybridAgentManager
from typing import Dict, Any

class IntentClassificationAgent:
    """Agent specialized in intent classification and message analysis"""
    
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        self.hybrid_manager = hybrid_manager or HybridAgentManager()
        self.name = "IntentClassificationAgent"
        self.agent_id = None
        self.initialized = False
        
        self.system_prompt = """You are an expert Intent Classification Agent specializing in understanding user intent and message classification.

Your expertise includes:
• Identifying user intent (question, request_help, information_seeking, task_planning, etc.)
• Classifying message types (casual_chat, urgent_request, information_query, emotional_support)
• Determining appropriate response approach
• Measuring message importance and priority levels
• Understanding conversation context and flow

When analyzing a message, provide classification in this format:
- Primary intent: [intent type]
- Message type: [message classification]
- Importance level: [low/medium/high/urgent]
- Priority score: [0.0-1.0]
- Requires immediate action: [yes/no]
- Suggested agent: [best agent for this request]
- Confidence: [0.0-1.0]

Available intents: question, request_help, casual_chat, task_planning, information_seeking, emotional_support, status_check, scheduling"""

    def initialize(self) -> bool:
        """Initialize the intent classification agent"""
        try:
            agent_data = self.hybrid_manager.create_agent(
                self.name,
                self.system_prompt,
                use_gemini=True  # This is for create_agent, not send_message
            )
            
            if agent_data and 'id' in agent_data:
                self.agent_id = agent_data['id']
                self.initialized = True
                print(f"✅ {self.name} initialized successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ {self.name} initialization failed: {e}")
            return False
    
    def classify_intent(self, message: str, emotional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Classify user intent using AI agent instead of hardcoded rules"""
        if not self.initialized:
            return {"intent": "unknown", "error": "Agent not initialized"}
        
        context_info = ""
        if emotional_context and emotional_context.get('emotions'):
            emotions = emotional_context.get('emotions', {})
            emotion_list = [f"{emotion}: {score:.1f}" for emotion, score in emotions.items()]
            context_info = f"\nEmotional context detected: {', '.join(emotion_list)}"
        
        classification_prompt = f"""Analyze the user intent and classify this message:
        
Message: "{message}"{context_info}

Provide comprehensive intent classification including primary intent, message type, importance level, priority score, and suggested agent."""
        
        try:
            # FIXED: Removed use_gemini parameter
            response = self.hybrid_manager.send_message(self.agent_id, classification_prompt)
            
            response_text = response.get('response', '')
            
            # Parse the response into structured format
            return self._parse_intent_classification(response_text, message, emotional_context)
                
        except Exception as e:
            print(f"⚠️ Intent classification failed: {e}")
            # Fallback to basic classification
            return self._fallback_intent_classification(message, emotional_context)
    
    def _parse_intent_classification(self, response_text: str, message: str, emotional_context: Dict = None) -> Dict[str, Any]:
        """Parse agent response into structured intent classification"""
        try:
            response_lower = response_text.lower()
            message_lower = message.lower()
            
            # Extract intent
            intent = "general"
            if 'question' in response_lower or '?' in message:
                intent = "question"
            elif 'help' in response_lower or 'request_help' in response_lower:
                intent = "request_help"
            elif 'schedule' in response_lower or 'meeting' in message_lower:
                intent = "scheduling"
            elif 'task' in response_lower or 'planning' in response_lower:
                intent = "task_planning"
            elif 'emotional' in response_lower or 'support' in response_lower:
                intent = "emotional_support"
            
            # Extract importance
            importance = 0.5
            if 'urgent' in response_lower or 'high' in response_lower:
                importance = 0.9
            elif 'medium' in response_lower:
                importance = 0.6
            elif 'low' in response_lower:
                importance = 0.3
            
            # Adjust based on emotional context
            if emotional_context and emotional_context.get('emotions'):
                if emotional_context.get('emotions', {}).get('urgency', 0) > 0.7:
                    importance = max(importance, 0.8)
                if emotional_context.get('emotions', {}).get('stress', 0) > 0.6:
                    importance = max(importance, 0.7)
            
            # Suggest appropriate agent
            suggested_agent = "ContextAgent"  # Default
            if emotional_context and emotional_context.get('emotions'):
                emotions = emotional_context.get('emotions', {})
                if emotions.get('stress', 0) > 0.6:
                    suggested_agent = "StressManagementAgent"
                elif emotions.get('seeking_help', 0) > 0.5 and 'task' in message_lower:
                    suggested_agent = "ProductivityAgent"
            
            if 'communication' in response_lower or 'conversation' in message_lower:
                suggested_agent = "CommunicationAgent"
            elif 'task' in message_lower or 'organize' in message_lower:
                suggested_agent = "ProductivityAgent"
            
            return {
                "intent": intent,
                "message_type": "urgent_request" if importance > 0.8 else "general",
                "importance": importance,
                "priority": "high" if importance > 0.8 else "medium",
                "requires_action": intent in ["request_help", "task_planning", "scheduling", "emotional_support"],
                "suggested_agent": suggested_agent,
                "confidence": 0.8,
                "analysis_text": response_text
            }
            
        except Exception:
            return self._fallback_intent_classification(message, emotional_context)
    
    def _fallback_intent_classification(self, message: str, emotional_context: Dict = None) -> Dict[str, Any]:
        """Fallback classification using keyword matching"""
        message_lower = message.lower()
        
        # Determine intent based on message content
        intent = "general"
        if '?' in message or any(word in message_lower for word in ['what', 'how', 'why', 'when', 'where']):
            intent = "question"
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            intent = "request_help"
        elif any(word in message_lower for word in ['schedule', 'meeting', 'appointment']):
            intent = "scheduling"
        elif any(word in message_lower for word in ['task', 'todo', 'organize']):
            intent = "task_planning"
        
        # Determine importance
        importance = 0.5
        if any(word in message_lower for word in ['urgent', 'important', 'emergency']):
            importance = 0.8
        elif any(word in message_lower for word in ['help', 'problem', 'issue']):
            importance = 0.7
        
        # Adjust based on emotional context
        if emotional_context and emotional_context.get('emotions'):
            emotions = emotional_context.get('emotions', {})
            if emotions.get('urgency', 0) > 0.7:
                importance = max(importance, 0.9)
            if emotions.get('stress', 0) > 0.6:
                importance = max(importance, 0.7)
        
        # Suggest agent
        suggested_agent = "ContextAgent"
        if emotional_context and emotional_context.get('emotions', {}).get('stress', 0) > 0.6:
            suggested_agent = "StressManagementAgent"
        elif 'task' in message_lower or 'organize' in message_lower:
            suggested_agent = "ProductivityAgent"
        elif 'conversation' in message_lower or 'communication' in message_lower:
            suggested_agent = "CommunicationAgent"
        
        return {
            "intent": intent,
            "message_type": "urgent_request" if importance > 0.8 else "general",
            "importance": importance,
            "priority": "high" if importance > 0.8 else "medium",
            "requires_action": intent in ["request_help", "task_planning", "scheduling"],
            "suggested_agent": suggested_agent,
            "confidence": 0.7,
            "analysis_text": "Fallback analysis used"
        }
