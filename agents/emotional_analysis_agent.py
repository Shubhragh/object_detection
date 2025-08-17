"""
Emotional Analysis Agent for AI Life Operating System
Specialized in detecting and analyzing emotional context from user messages
"""

from hybrid_agent_manager import HybridAgentManager
from typing import Dict, Any

class EmotionalAnalysisAgent:
    """Agent specialized in emotional context analysis"""
    
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        self.hybrid_manager = hybrid_manager or HybridAgentManager()
        self.name = "EmotionalAnalysisAgent"
        self.agent_id = None
        self.initialized = False
        
        # Specialized system prompt for emotional analysis
        self.system_prompt = """You are an expert Emotional Analysis Agent specializing in detecting and analyzing emotional context from user messages.

Your expertise includes:
• Identifying emotional states (stress, anxiety, happiness, frustration, excitement, etc.)
• Measuring emotional intensity levels (0.0 to 1.0 scale)
• Detecting urgency and help-seeking behaviors
• Recognizing learning curiosity and engagement levels
• Understanding contextual emotional nuances

When analyzing a message, provide your analysis in this format:
- Primary emotions detected: [emotion]: [intensity 0.0-1.0]
- Secondary emotions: [if any]
- Overall emotional intensity: [0.0-1.0]
- Help-seeking behavior: [yes/no with confidence]
- Urgency level: [low/medium/high]

Always be specific about emotion types and intensity levels."""

    def initialize(self) -> bool:
        """Initialize the emotional analysis agent"""
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
    
    def analyze_emotional_context(self, message: str) -> Dict[str, Any]:
        """Analyze emotional context using AI agent instead of hardcoded rules"""
        if not self.initialized:
            return {"emotions": {}, "error": "Agent not initialized"}
        
        analysis_prompt = f"""Analyze the emotional context of this user message:
        
Message: "{message}"

Provide detailed emotional analysis including all detected emotions with intensity scores, help-seeking behavior, and urgency level."""
        
        try:
            # FIXED: Removed use_gemini parameter
            response = self.hybrid_manager.send_message(self.agent_id, analysis_prompt)
            
            response_text = response.get('response', '')
            
            # Parse the response into structured format
            return self._parse_emotional_analysis(response_text, message)
                
        except Exception as e:
            print(f"⚠️ Emotional analysis failed: {e}")
            # Fallback to basic keyword analysis
            return self._fallback_emotional_analysis(message)
    
    def _parse_emotional_analysis(self, response_text: str, message: str) -> Dict[str, Any]:
        """Parse agent response into structured emotional analysis"""
        emotions = {}
        primary_emotion = "neutral"
        intensity = 0.0
        
        try:
            response_lower = response_text.lower()
            
            # Extract emotions from response
            emotion_keywords = {
                'stress': ['stress', 'stressed', 'overwhelm', 'pressure', 'tension'],
                'seeking_help': ['help', 'assist', 'support', 'guidance', 'confused'],
                'positive': ['happy', 'excited', 'pleased', 'satisfied', 'joy'],
                'negative': ['sad', 'upset', 'frustrated', 'disappointed', 'angry'],
                'urgency': ['urgent', 'immediate', 'emergency', 'asap', 'quickly'],
                'curiosity': ['curious', 'learning', 'understand', 'explain', 'question']
            }
            
            # Extract intensity values from response
            for emotion, keywords in emotion_keywords.items():
                if any(keyword in response_lower for keyword in keywords):
                    # Try to extract numerical intensity
                    if 'high' in response_lower or 'strong' in response_lower:
                        emotions[emotion] = 0.8
                    elif 'medium' in response_lower or 'moderate' in response_lower:
                        emotions[emotion] = 0.6
                    elif 'low' in response_lower or 'mild' in response_lower:
                        emotions[emotion] = 0.4
                    else:
                        emotions[emotion] = 0.7
            
            # Determine primary emotion
            if emotions:
                primary_emotion = max(emotions, key=emotions.get)
                intensity = emotions[primary_emotion]
        
        except Exception:
            pass
        
        return {
            "emotions": emotions,
            "primary_emotion": primary_emotion,
            "intensity": intensity,
            "confidence": 0.8 if emotions else 0.5,
            "analysis_text": response_text
        }
    
    def _fallback_emotional_analysis(self, message: str) -> Dict[str, Any]:
        """Fallback emotional analysis using keyword matching"""
        emotions = {}
        message_lower = message.lower()
        
        # Basic keyword detection
        if any(word in message_lower for word in ['stress', 'stressed', 'overwhelmed', 'pressure']):
            emotions['stress'] = 0.7
        
        if any(word in message_lower for word in ['help', 'assist', 'support', 'guidance']):
            emotions['seeking_help'] = 0.6
        
        if any(word in message_lower for word in ['happy', 'great', 'awesome', 'excited']):
            emotions['positive'] = 0.6
        
        if any(word in message_lower for word in ['sad', 'upset', 'frustrated', 'disappointed']):
            emotions['negative'] = 0.6
        
        if any(word in message_lower for word in ['urgent', 'immediately', 'asap', 'emergency']):
            emotions['urgency'] = 0.8
        
        if any(word in message_lower for word in ['learn', 'understand', 'explain', 'curious']):
            emotions['curiosity'] = 0.5
        
        primary_emotion = max(emotions, key=emotions.get) if emotions else "neutral"
        intensity = emotions.get(primary_emotion, 0.0)
        
        return {
            "emotions": emotions,
            "primary_emotion": primary_emotion,
            "intensity": intensity,
            "confidence": 0.6,
            "analysis_text": "Fallback analysis used"
        }
