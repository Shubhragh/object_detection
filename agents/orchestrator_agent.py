"""
ENHANCED Orchestrator Agent with Response Humanization Integration
"""

import sys
import os

from agents.base_agent import BaseAgent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_agent_manager import HybridAgentManager
from typing import List, Dict, Any
import time
import json

class OrchestratorAgent:
    def __init__(self, use_gemini: bool = True):
        # Enhanced system prompt for intelligent routing
        system_prompt = """You are an intelligent AI coordinator who routes conversations to the best specialist. You understand context, intent, and nuance - not just keywords.

AVAILABLE SPECIALISTS:
- StressManagementAgent: Emotional support, mental wellness, stress, anxiety, confusion, sadness, overwhelm, personal struggles
- ProductivityAgent: Work efficiency, time management, task organization, goal setting, planning, deadlines, workflow optimization
- CommunicationAgent: Relationships, social situations, conversation help, conflict resolution, interpersonal advice
- ContextAgent: General knowledge, information requests, explanations, analysis, creative tasks, problem-solving, casual conversation, system queries about memory/experiences

ROUTING INTELLIGENCE:
- Understand the INTENT behind messages, not just surface words
- Consider emotional context and underlying needs
- Route based on what the user actually needs help with
- PRIORITY: System queries about memory/experiences go to ContextAgent
- Default to ContextAgent for general, informational, or creative queries

RESPONSE FORMAT:
**Selected Agent:** [EXACT agent name]
**Reasoning:** [Why this agent is best suited for this specific need]

Think about what the user truly needs, not just what words they used."""

        self.hybrid_manager = HybridAgentManager()
        self.name = "OrchestratorAgent"
        self.system_prompt = system_prompt
        self.use_gemini = use_gemini
        self.agent_id = None

        # Enhanced tracking and humanizer integration
        self.available_agents = {}
        self.response_humanizer = None
        self.system_state = {
            "total_routes": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "last_route_time": 0,
            "route_distribution": {
                "StressManagementAgent": 0,
                "ProductivityAgent": 0,
                "CommunicationAgent": 0,
                "ContextAgent": 0
            }
        }

        print(f"🎯 Enhanced Orchestrator Agent initialized")

    def initialize(self) -> bool:
        """Initialize the orchestrator and create specialized agents"""
        try:
            # Create orchestrator agent
            agent_data = self.hybrid_manager.create_agent(
                self.name,
                self.system_prompt,
                use_gemini=self.use_gemini
            )

            if not agent_data or not agent_data.get('id'):
                print(f"❌ Orchestrator agent creation failed")
                return False

            self.agent_id = agent_data['id']
            print(f"✅ Orchestrator agent created: {self.agent_id}")

            # Initialize specialized agents
            self._initialize_specialized_agents()

            # IMPORTANT: Initialize Response Humanizer
            self._initialize_response_humanizer()

            print(f"✅ Orchestrator initialized with {len(self.available_agents)} specialized agents")
            return True

        except Exception as e:
            print(f"❌ Orchestrator initialization failed: {e}")
            return False

    def _initialize_specialized_agents(self):
        """Create and register all specialized agents"""
        try:
            # Import specialized agents
            from agents.stress_agent import StressManagementAgent
            from agents.productivity_agent import ProductivityAgent
            from agents.communication_agent import CommunicationOptimizationAgent
            from agents.context_agent import ContextAnalysisAgent

            # Define agents to create
            agents_to_create = [
                ("StressManagementAgent", StressManagementAgent),
                ("ProductivityAgent", ProductivityAgent),
                ("CommunicationAgent", CommunicationOptimizationAgent),
                ("ContextAgent", ContextAnalysisAgent)
            ]

            for agent_name, agent_class in agents_to_create:
                try:
                    # Create agent instance
                    agent_instance = agent_class(self.hybrid_manager)
                    
                    if agent_instance.initialize():
                        self.available_agents[agent_name] = {
                            'instance': agent_instance,
                            'id': agent_instance.agent_id,
                            'name': agent_name,
                            'active': True,
                            'created_time': time.time(),
                            'successful_tasks': 0
                        }
                        print(f"✅ Registered {agent_name} with ID: {agent_instance.agent_id}")
                    else:
                        print(f"❌ Failed to initialize {agent_name}")

                except Exception as e:
                    print(f"❌ Error creating {agent_name}: {e}")

            if not self.available_agents:
                print("⚠️ No specialized agents were successfully created")

        except Exception as e:
            print(f"❌ Specialized agent initialization failed: {e}")
            self.available_agents = {}

    def _initialize_response_humanizer(self):
        """Initialize the Response Humanizer Agent"""
        try:
            from agents.response_humanizer_agent import ResponseHumanizerAgent
            
            self.response_humanizer = ResponseHumanizerAgent(self.hybrid_manager)
            if self.response_humanizer.initialize():
                print("✅ Response Humanizer integrated successfully")
            else:
                print("⚠️ Response Humanizer failed to initialize - responses will be less natural")
                self.response_humanizer = None

        except Exception as e:
            print(f"⚠️ Response Humanizer integration failed: {e}")
            self.response_humanizer = None

    def route_message(self, message: str) -> Dict[str, Any]:
        """ENHANCED: Intelligent routing with response humanization"""
        start_time = time.time()
        self.system_state["total_routes"] += 1

        try:
            print(f"🎯 Orchestrator analyzing: '{message[:60]}{'...' if len(message) > 60 else ''}'")

            # Step 1: AI-powered intelligent routing
            ai_decision = self._get_ai_routing_decision(message)
            selected_agent = ai_decision.get('agent')
            reasoning = ai_decision.get('reasoning', 'AI routing decision')

            print(f"🧠 AI analysis: {selected_agent} - {reasoning}")

            # Step 2: Execute on AI-selected agent
            if selected_agent and selected_agent in self.available_agents:
                agent_response = self._execute_agent_task(selected_agent, message)
                
                if agent_response.get('success'):
                    # Update routing statistics
                    self.system_state["successful_routes"] += 1
                    self.system_state["last_route_time"] = time.time()
                    self.system_state["route_distribution"][selected_agent] += 1
                    self.available_agents[selected_agent]["successful_tasks"] += 1
                    
                    # HUMANIZE RESPONSE
                    final_response = self._humanize_agent_response(
                        agent_response.get('response', ''), 
                        message
                    )
                    
                    return {
                        "routing_success": True,
                        "routed_to": selected_agent,
                        "agent_response": final_response,
                        "reasoning": reasoning,
                        "response_time": time.time() - start_time,
                        "routing_confidence": "high",
                        "humanized": bool(self.response_humanizer)
                    }
                else:
                    print(f"❌ Agent {selected_agent} execution failed: {agent_response.get('error', 'Unknown error')}")

            # Step 3: Intelligent fallback with context analysis
            print(f"🔄 Primary routing failed, analyzing message context for fallback")
            fallback_agent = self._intelligent_fallback_selection(message)
            
            if fallback_agent and fallback_agent in self.available_agents:
                print(f"🎯 Smart fallback to {fallback_agent}")
                agent_response = self._execute_agent_task(fallback_agent, message)
                
                if agent_response.get('success'):
                    self.system_state["successful_routes"] += 1
                    self.system_state["route_distribution"][fallback_agent] += 1
                    
                    # HUMANIZE FALLBACK RESPONSE
                    final_response = self._humanize_agent_response(
                        agent_response.get('response', ''), 
                        message
                    )
                    
                    return {
                        "routing_success": True,
                        "routed_to": fallback_agent,
                        "agent_response": final_response,
                        "reasoning": "Intelligent fallback analysis",
                        "response_time": time.time() - start_time,
                        "routing_confidence": "medium",
                        "humanized": bool(self.response_humanizer)
                    }

            # Step 4: Default to ContextAgent for general queries
            if 'ContextAgent' in self.available_agents:
                print(f"🔄 Routing to ContextAgent as general-purpose handler")
                agent_response = self._execute_agent_task('ContextAgent', message)
                
                if agent_response.get('success'):
                    self.system_state["successful_routes"] += 1
                    self.system_state["route_distribution"]['ContextAgent'] += 1
                    
                    # HUMANIZE CONTEXT AGENT RESPONSE
                    final_response = self._humanize_agent_response(
                        agent_response.get('response', ''), 
                        message
                    )
                    
                    return {
                        "routing_success": True,
                        "routed_to": "ContextAgent",
                        "agent_response": final_response,
                        "reasoning": "Default context agent handling",
                        "response_time": time.time() - start_time,
                        "routing_confidence": "low",
                        "humanized": bool(self.response_humanizer)
                    }

            # Step 5: Emergency orchestrator response
            print(f"⚠️ All agents unavailable, generating direct response")
            direct_response = self._generate_direct_response(message)
            
            # HUMANIZE DIRECT RESPONSE
            final_response = self._humanize_agent_response(direct_response, message)
            
            self.system_state["failed_routes"] += 1
            
            return {
                "routing_success": False,
                "routed_to": "orchestrator",
                "response": final_response,
                "reasoning": "Emergency direct response - all agents unavailable",
                "response_time": time.time() - start_time,
                "routing_confidence": "emergency",
                "humanized": bool(self.response_humanizer)
            }

        except Exception as e:
            print(f"❌ Routing failed with exception: {e}")
            self.system_state["failed_routes"] += 1
            
            return {
                "routing_success": False,
                "routed_to": "orchestrator",
                "response": "I apologize, but I'm experiencing technical difficulties. Please try rephrasing your question and I'll do my best to help.",
                "error": str(e),
                "response_time": time.time() - start_time
            }

    def _humanize_agent_response(self, original_response: str, user_message: str) -> str:
        """Humanize the agent response to sound natural and warm"""
        if not self.response_humanizer:
            return original_response

        try:
            user_emotion = self.response_humanizer.detect_user_emotion(user_message)
            print(f"🎭 Humanizing response (detected emotion: {user_emotion})")
            
            humanized_response = self.response_humanizer.humanize_response(
                original_response, 
                user_message, 
                user_emotion
            )
            
            return humanized_response
            
        except Exception as e:
            print(f"⚠️ Response humanization failed: {e}")
            return original_response

    def _get_ai_routing_decision(self, message: str) -> Dict[str, str]:
        """Enhanced AI routing with better prompting"""
        try:
            routing_prompt = f"""
USER MESSAGE: "{message}"

Analyze this message holistically. Consider:
- What does the user ACTUALLY need help with?
- What's the underlying intent or goal?
- What type of response would be most helpful?
- What expertise is required?

AVAILABLE SPECIALISTS:
- StressManagementAgent: Emotional support, mental wellness, personal struggles
- ProductivityAgent: Work efficiency, organization, planning, time management  
- CommunicationAgent: Relationships, social situations, interpersonal advice
- ContextAgent: General knowledge, explanations, information, casual conversation, creative tasks, SYSTEM QUERIES about memory/experiences

PRIORITY ROUTING:
- Questions about "stored experiences", "memory", "previous conversations" → ContextAgent
- Emotional distress, stress, sadness → StressManagementAgent
- Work, tasks, productivity → ProductivityAgent
- Relationships, social issues → CommunicationAgent
- General questions, information → ContextAgent

Choose the specialist who can provide the MOST HELPFUL response to this specific user need.

RESPOND WITH:
**Selected Agent:** [EXACT agent name]
**Reasoning:** [Why this specialist is the best match for what the user needs]
"""

            response = self.hybrid_manager.send_message(self.agent_id, routing_prompt)
            
            if response.get('success'):
                ai_response = response.get('response', '')
                selected_agent = self._parse_agent_decision(ai_response, message)
                reasoning = self._parse_reasoning(ai_response)

                return {
                    'agent': selected_agent,
                    'reasoning': reasoning,
                    'ai_response': ai_response
                }
            else:
                print(f"⚠️ AI routing request failed: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"⚠️ AI routing decision failed: {e}")

        # Fallback to intelligent analysis
        return {
            'agent': self._intelligent_fallback_selection(message),
            'reasoning': 'Fallback due to AI routing failure'
        }

    def _parse_agent_decision(self, ai_response: str, original_message: str) -> str:
        """CORRECTED: Enhanced agent decision parsing with memory query priority"""
        try:
            response_lower = ai_response.lower()
            message_lower = original_message.lower()
            
            # PRIORITY: System/memory queries go to ContextAgent FIRST
            if any(word in message_lower for word in ['stored', 'experiences', 'memory', 'remember', 'previous', 'history', 'what do you know', 'what are my']):
                return 'ContextAgent'
            
            # Look for exact agent names
            if 'stressmanagementagent' in response_lower or 'stress management' in response_lower:
                return 'StressManagementAgent'
            elif 'productivityagent' in response_lower or 'productivity' in response_lower:
                return 'ProductivityAgent'
            elif 'communicationagent' in response_lower or 'communication' in response_lower:
                return 'CommunicationAgent'
            elif 'contextagent' in response_lower or 'context' in response_lower:
                return 'ContextAgent'
            
            # Intelligent context analysis fallback
            return self._intelligent_fallback_selection(original_message)
                
        except Exception as e:
            print(f"⚠️ Agent parsing failed: {e}")
            return self._intelligent_fallback_selection(original_message)

    def _intelligent_fallback_selection(self, message: str) -> str:
        """CORRECTED: Enhanced context-aware fallback with memory query priority"""
        try:
            message_lower = message.lower()
            
            # PRIORITY: System/memory queries (HIGHEST PRIORITY)
            if any(word in message_lower for word in ['stored', 'experiences', 'memory', 'remember', 'previous', 'history', 'what do you know', 'what are my']):
                if 'ContextAgent' in self.available_agents:
                    return 'ContextAgent'
            
            # Check for negative emotional states (HIGH PRIORITY)
            if any(pattern in message_lower for pattern in ['sad', 'depressed', 'anxious', 'stressed', 'overwhelmed', 'upset', 'struggling', 'difficult', 'tough', 'worried', 'confused', 'lost']):
                if 'StressManagementAgent' in self.available_agents:
                    return 'StressManagementAgent'
            
            # Check for work/productivity needs
            productivity_patterns = [
                'work', 'job', 'task', 'deadline', 'schedule', 'time', 'organize',
                'productivity', 'efficient', 'planning', 'goal', 'project',
                'manage', 'workflow', 'busy', 'priority', 'calendar'
            ]
            if any(pattern in message_lower for pattern in productivity_patterns):
                if 'ProductivityAgent' in self.available_agents:
                    return 'ProductivityAgent'
            
            # Check for social/communication needs
            communication_patterns = [
                'relationship', 'friend', 'family', 'colleague', 'boss', 'partner',
                'conversation', 'talk', 'communicate', 'social', 'conflict',
                'argument', 'disagreement', 'advice', 'dating', 'marriage'
            ]
            if any(pattern in message_lower for pattern in communication_patterns):
                if 'CommunicationAgent' in self.available_agents:
                    return 'CommunicationAgent'
            
            # Default: ContextAgent handles general queries, information requests, explanations
            if 'ContextAgent' in self.available_agents:
                return 'ContextAgent'
            
            # Return any available agent as final fallback
            available_agents = list(self.available_agents.keys())
            return available_agents[0] if available_agents else None
            
        except Exception as e:
            print(f"⚠️ Intelligent fallback failed: {e}")
            return 'ContextAgent' if 'ContextAgent' in self.available_agents else None

    def _parse_reasoning(self, ai_response: str) -> str:
        """Extract reasoning from AI response"""
        try:
            lines = ai_response.split('\n')
            for line in lines:
                if 'reasoning:' in line.lower():
                    return line.split(':', 1)[1].strip()
        except:
            pass
        return "AI routing analysis"

    def _execute_agent_task(self, agent_name: str, message: str) -> Dict[str, Any]:
        """Execute task with proper success checking"""
        try:
            agent_data = self.available_agents.get(agent_name)
            if not agent_data:
                print(f"❌ Agent {agent_name} not found in registry")
                return {"success": False, "error": f"Agent {agent_name} not available"}

            agent_id = agent_data.get('id')
            if not agent_id:
                print(f"❌ Agent {agent_name} has no valid ID")
                return {"success": False, "error": f"Agent {agent_name} has no valid ID"}

            print(f"🎯 Executing task on {agent_name} (ID: {agent_id})")
            
            # Send message through hybrid manager
            result = self.hybrid_manager.send_message(agent_id, message)
            
            # Check success properly
            if result.get('success') is True:
                print(f"✅ Agent {agent_name} responded successfully")
                return {
                    "success": True,
                    "response": result.get('response', ''),
                    "agent": agent_name,
                    "agent_id": agent_id
                }
            else:
                error_msg = result.get('error', 'Agent response failed')
                print(f"❌ Agent {agent_name} execution failed: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "agent": agent_name
                }

        except Exception as e:
            print(f"❌ Agent execution exception for {agent_name}: {e}")
            return {"success": False, "error": str(e), "agent": agent_name}

    def _generate_direct_response(self, message: str) -> str:
        """Generate helpful direct response for any type of query"""
        try:
            direct_prompt = f"""
The user said: "{message}"

As a helpful AI assistant, provide a natural, supportive response that addresses their message appropriately. Be conversational, empathetic, and genuinely helpful. Match their tone and provide value based on what they're asking or sharing.
"""
            response = self.hybrid_manager.send_message(self.agent_id, direct_prompt)
            
            if response.get('success'):
                return response.get('response', 'I understand your message. How can I help you today?')
            else:
                return "I understand what you're saying. While I'm having some technical difficulties right now, I'm here to help. Could you tell me a bit more about what you need?"
                
        except Exception as e:
            print(f"⚠️ Direct response generation failed: {e}")
            return "I'm here to help with whatever you need. Could you tell me more about your question or what's on your mind?"

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator system status"""
        return {
            "orchestrator": {
                "name": self.name,
                "agent_id": self.agent_id,
                "initialized": bool(self.agent_id)
            },
            "available_agents": list(self.available_agents.keys()),
            "response_humanizer": bool(self.response_humanizer),
            "system_metrics": self.system_state,
            "routing_success_rate": (
                (self.system_state["successful_routes"] / max(1, self.system_state["total_routes"])) * 100
            ),
            "route_distribution": self.system_state["route_distribution"]
        }

# Test the enhanced orchestrator
if __name__ == "__main__":
    print("🧪 Testing Enhanced Orchestrator Agent...")
    
    orchestrator = OrchestratorAgent(use_gemini=True)
    
    if orchestrator.initialize():
        print("✅ Orchestrator initialized successfully")
        
        # Test various types of queries
        test_messages = [
            "What are my previous experiences stored for user",
            "I am feeling stressed out",
            "I'm really happy today!",
            "How do I organize my schedule?",
            "What's the capital of France?"
        ]
        
        for msg in test_messages:
            result = orchestrator.route_message(msg)
            print(f"✅ '{msg[:30]}...' → {result.get('routed_to')} (humanized: {result.get('humanized', False)})")
        
        print("🎉 Enhanced Orchestrator test complete!")
    else:
        print("❌ Orchestrator initialization failed")
