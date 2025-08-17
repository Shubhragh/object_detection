"""
Response Humanizer Agent - Makes AI responses sound natural, warm, and human-like
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_agent_manager import HybridAgentManager
from typing import Dict, Any, List
import time
import re
from agents.base_agent import BaseAgent

class ResponseHumanizerAgent:
    def __init__(self, hybrid_manager: HybridAgentManager = None):
        self.hybrid_manager = hybrid_manager or HybridAgentManager()
        self.name = "ResponseHumanizerAgent"
        self.agent_id = None
        
        # ENHANCED: Natural conversation system prompt
        self.system_prompt = """You are a master conversationalist who transforms robotic AI responses into warm, natural, human-like conversations.

Your specialty is rewriting AI responses to sound like they come from a caring, intelligent friend who:
- Speaks naturally with contractions, varied sentence lengths, and casual language
- Shows genuine empathy and understanding
- Matches the user's energy and communication style
- Uses conversational phrases like "I get it," "That makes sense," "Here's the thing"
- Avoids corporate/formal language, templates, and robotic phrases
- Includes natural hesitations, thoughts, and personal touches
- Responds authentically to emotions - excited when they're excited, gentle when they're sad

TRANSFORMATION RULES:
- Remove phrases like "I understand that" → "I get it" or just jump into the response
- Replace "I recommend" → "You might try" or "What works well is"
- Change "Please feel free to" → "Go ahead and" or just give direct guidance
- Transform lists into conversational flow
- Add personality and warmth without losing the helpful information

Make every response feel like a natural conversation with someone who truly cares."""

        print("🎭 Response Humanizer Agent initialized")

    def initialize(self) -> bool:
        """Initialize the humanizer agent"""
        try:
            agent_data = self.hybrid_manager.create_agent(
                self.name,
                self.system_prompt,
                use_gemini=True  # Use Gemini for better natural language generation
            )

            if agent_data and agent_data.get('id'):
                self.agent_id = agent_data['id']
                print(f"✅ Response Humanizer initialized: {self.agent_id}")
                return True
            
            print("❌ Response Humanizer agent creation failed")
            return False

        except Exception as e:
            print(f"❌ Response Humanizer initialization failed: {e}")
            return False

    def humanize_response(self, original_response: str, user_message: str, 
                         user_emotion: str = "neutral", conversation_context: List = None) -> str:
        """Transform robotic response into natural, human-like conversation"""
        
        if not self.agent_id:
            return self._fallback_humanize(original_response)

        try:
            # Build context-aware humanization prompt
            humanization_prompt = f"""
USER'S MESSAGE: "{user_message}"
USER'S EMOTIONAL STATE: {user_emotion}
ORIGINAL AI RESPONSE: "{original_response}"

Transform this response to sound like a caring friend would naturally respond. Consider:
- The user's emotional state and match the appropriate energy
- Make it conversational and warm, not formal or robotic
- Keep all the helpful information but present it naturally
- Use the user's communication style (casual, formal, etc.)
- Remove any corporate-speak or template language

NATURAL, HUMANIZED RESPONSE:"""

            response = self.hybrid_manager.send_message(self.agent_id, humanization_prompt)
            
            if response.get('success') and response.get('response'):
                humanized = response.get('response', '').strip()
                
                # Additional post-processing
                humanized = self._apply_conversational_polish(humanized)
                
                print(f"🎭 Response humanized successfully")
                return humanized
            else:
                print(f"⚠️ Humanization failed: {response.get('error', 'Unknown error')}")
                return self._fallback_humanize(original_response)

        except Exception as e:
            print(f"⚠️ Humanization error: {e}")
            return self._fallback_humanize(original_response)

    def _apply_conversational_polish(self, text: str) -> str:
        """Apply final conversational polish to humanized text"""
        
        # Basic contractions
        contractions = {
            r'\bI am\b': "I'm",
            r'\byou are\b': "you're", 
            r'\bwe are\b': "we're",
            r'\bthey are\b': "they're",
            r'\bit is\b': "it's",
            r'\bthat is\b': "that's",
            r'\bwhat is\b': "what's",
            r'\bhere is\b': "here's",
            r'\bthere is\b': "there's",
            r'\bdo not\b': "don't",
            r'\bdoes not\b': "doesn't", 
            r'\bdid not\b': "didn't",
            r'\bcannot\b': "can't",
            r'\bwill not\b': "won't",
            r'\bwould not\b': "wouldn't",
            r'\bshould not\b': "shouldn't",
            r'\bcould not\b': "couldn't",
            r'\bis not\b': "isn't",
            r'\bare not\b': "aren't",
            r'\bwas not\b': "wasn't",
            r'\bwere not\b': "weren't",
            r'\bhave not\b': "haven't",
            r'\bhas not\b': "hasn't",
            r'\bhad not\b': "hadn't"
        }
        
        # Apply contractions
        for formal, casual in contractions.items():
            text = re.sub(formal, casual, text, flags=re.IGNORECASE)
        
        # Remove overly formal phrases
        formal_replacements = {
            "I would be happy to": "I'd love to",
            "I would recommend": "I'd suggest",
            "Please feel free to": "Go ahead and",
            "I understand that you": "I get that you",
            "I want to help you": "Let me help you",
            "I hope this helps": "Hope this helps",
            "Thank you for sharing": "Thanks for sharing"
        }
        
        for formal, casual in formal_replacements.items():
            text = text.replace(formal, casual)
        
        return text

    def _fallback_humanize(self, text: str) -> str:
        """Simple fallback humanization when AI processing fails"""
        
        # Apply basic conversational improvements
        text = self._apply_conversational_polish(text)
        
        # Remove some robotic phrases
        robotic_replacements = {
            "I am here to assist you": "I'm here to help",
            "I understand your concern": "I get it",
            "I apologize for any inconvenience": "Sorry about that",
            "Please let me know if": "Just let me know if",
            "I hope this information is helpful": "Hope this helps",
            "Based on the information provided": "From what you've told me",
            "I would suggest that you": "You might want to",
            "It is important to note that": "Keep in mind that"
        }
        
        for robotic, natural in robotic_replacements.items():
            text = text.replace(robotic, natural)
        
        return text

    def detect_user_emotion(self, message: str) -> str:
        """Simple emotion detection to help with response tone"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['excited', 'happy', 'great', 'awesome', 'amazing', 'fantastic']):
            return "excited"
        elif any(word in message_lower for word in ['sad', 'upset', 'down', 'depressed', 'disappointed']):
            return "sad"
        elif any(word in message_lower for word in ['stressed', 'anxious', 'worried', 'overwhelmed', 'panic']):
            return "stressed"
        elif any(word in message_lower for word in ['confused', 'unsure', 'lost', 'stuck']):
            return "confused"
        elif any(word in message_lower for word in ['angry', 'frustrated', 'annoyed', 'mad']):
            return "frustrated"
        else:
            return "neutral"

# Test the humanizer
if __name__ == "__main__":
    print("🧪 Testing Response Humanizer Agent...")
    
    humanizer = ResponseHumanizerAgent()
    
    if humanizer.initialize():
        # Test with robotic response
        robotic_response = """I understand that you are feeling stressed about work deadlines. I recommend that you implement the following strategies: 1) Create a prioritized task list, 2) Break large projects into smaller tasks, 3) Use time-blocking techniques. Please feel free to reach out if you need additional assistance with productivity optimization."""
        
        user_message = "I'm so stressed about all these work deadlines"
        user_emotion = humanizer.detect_user_emotion(user_message)
        
        humanized = humanizer.humanize_response(robotic_response, user_message, user_emotion)
        
        print(f"\n📋 Original: {robotic_response}")
        print(f"\n🎭 Humanized: {humanized}")
        print("\n🎉 Response Humanizer test complete!")
    else:
        print("❌ Response Humanizer initialization failed")
