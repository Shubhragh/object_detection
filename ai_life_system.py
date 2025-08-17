"""
AI Life Operating System - Production Version
Complete autonomous AI assistant with memory, relationships, and proactive intelligence
"""

from hybrid_agent_manager import HybridAgentManager
from agent_network import AILifeAgentNetwork
from events.event_manager import EventManager
from memory import MemoryManager, PatternRecognitionEngine, RelationshipMemoryNetwork, MemoryConsolidationEngine
from proactive.proactive_intelligence import ProactiveIntelligenceEngine
from proactive.predictive_planner import PredictiveTaskPlanner
from proactive.autonomous_assistant import AutonomousAssistantManager
from integration.performance_optimizer import PerformanceOptimizer
from integration.health_monitor import SystemHealthMonitor
import time
import threading
from typing import Dict, Any

class AILifeOperatingSystem:
    def __init__(self):
        """Initialize AI Life Operating System with all components"""
        self.agent_network = AILifeAgentNetwork()
        self.event_manager = EventManager()
        
        # Core memory system with intelligence
        self.memory_manager = MemoryManager()
        self.pattern_engine = PatternRecognitionEngine(self.memory_manager)
        self.relationship_network = RelationshipMemoryNetwork(self.memory_manager)
        self.consolidation_engine = MemoryConsolidationEngine(self.memory_manager)
        
        # CRITICAL: Link consolidation engine to memory manager
        self.memory_manager.consolidation_engine = self.consolidation_engine
        
        # Proactive intelligence systems
        self.proactive_engine = ProactiveIntelligenceEngine(
            self.memory_manager, 
            self.pattern_engine, 
            self.consolidation_engine
        )
        self.predictive_planner = PredictiveTaskPlanner(self.memory_manager)
        self.autonomous_assistant = AutonomousAssistantManager()
        
        # System optimization and monitoring
        self.performance_optimizer = PerformanceOptimizer(self)
        self.health_monitor = SystemHealthMonitor(self)
        
        self.running = False
        print("🤖 AI Life Operating System initialized successfully")

    def initialize(self) -> bool:
        """Initialize and start all AI Life OS components"""
        print("🚀 Starting AI Life Operating System...")
        
        # Initialize agent network
        if not self.agent_network.initialize_network():
            print("❌ Agent network initialization failed")
            return False
        
        # Initialize autonomous assistant with agent network
        self.autonomous_assistant = AutonomousAssistantManager(
            self.agent_network, 
            self.memory_manager
        )
        
        # Start background systems
        self._start_background_systems()
        
        print("✅ AI Life OS fully operational")
        self.running = True
        return True
    
    def _start_background_systems(self):
        """Start background monitoring and optimization"""
        # Start event system
        self.event_manager.start_internal_clock(300)  # 5-minute intervals
        self._setup_event_handlers()
        
        # Start health monitoring
        self.health_monitor.start_monitoring()
        
        # Enable autonomous assistance
        self.autonomous_assistant.enable_autonomous_mode()
    
    def _setup_event_handlers(self):
        """Setup event handling for proactive intelligence"""
        def handle_periodic_check(event_data):
            try:
                # Run proactive analysis
                predictions = self.pattern_engine.predict_user_needs("user")
                
                if predictions.get('predictions'):
                    pattern_analysis = self.pattern_engine.analyze_all_patterns("user")
                    proactive_plan = self.proactive_engine._generate_proactive_plan(pattern_analysis, predictions)
                    
                    # Execute high-confidence proactive tasks
                    for task in proactive_plan:
                        if task.get('confidence', 0) > 0.8:
                            self.autonomous_assistant.execute_proactive_intervention(task, "user")
            
            except Exception as e:
                print(f"⚠️ Background analysis error: {e}")
        
        # Subscribe to events
        event_handler = self.event_manager.subscribe_to_events(handle_periodic_check)
        
        # Start event listener
        listener_thread = threading.Thread(target=event_handler)
        listener_thread.daemon = True
        listener_thread.start()
    
    def chat(self, message: str) -> str:
        """Main chat interface with intelligent routing and memory"""
        if not self.running:
            return "AI Life OS not initialized. Please restart the system."
        
        # Check performance cache first
        cached_response = self.performance_optimizer.get_cached_response(message)
        if cached_response:
            return cached_response
        
        start_time = time.time()
        
        try:
            # Analyze emotional context and importance
            emotional_context = self._detect_emotional_context(message)
            message_importance = self._calculate_message_importance(message, emotional_context)
            
            # Update relationship network
            try:
                self.relationship_network.update_relationship_from_interaction(
                    "user", message, emotional_context
                )
            except Exception:
                pass  # Continue if relationship update fails
            
            # Store user message in memory
            try:
                if hasattr(self.memory_manager, 'store_enhanced_experience'):
                    self.memory_manager.store_enhanced_experience(
                        "user",
                        {"type": "user_message", "message": message},
                        emotional_context,
                        message_importance
                    )
            except Exception:
                pass  # Continue if memory storage fails
            
            # Route message to appropriate agent
            routing_result = self.agent_network.orchestrator.route_message(message)
            
            if routing_result.get("routing_success"):
                routed_agent = routing_result.get('routed_to')
                
                # Get actual response from the routed agent
                actual_response = routing_result.get('agent_response', '')
                
                # If no agent response, get it directly
                if not actual_response:
                    agent_id = self.agent_network.agents.get(routed_agent.lower(), {}).get('id')
                    if agent_id:
                        direct_response = self.agent_network.hybrid_manager.send_message(
                            agent_id, message
                        )
                        actual_response = direct_response.get('response', 'I apologize, but I was unable to generate a response.')
                
                # Store response in memory
                try:
                    if hasattr(self.memory_manager, 'store_enhanced_experience'):
                        self.memory_manager.store_enhanced_experience(
                            "user",
                            {"type": "system_response", "message": actual_response},
                            {"helpfulness": 0.8, "engagement": 0.7},
                            0.6
                        )
                except Exception:
                    pass
                
                # Cache response and update performance metrics
                response_time = time.time() - start_time
                self.performance_optimizer.optimize_response_caching(message, actual_response)
                self.performance_optimizer.metrics["response_times"].append(response_time)
                
                return actual_response
            
            else:
                # Fallback routing
                response = self.agent_network.route_message(message)
                return response.get('response', 'I apologize, but I was unable to process your request. Please try rephrasing.')
                
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}. Please try again."
    
    def _detect_emotional_context(self, message: str) -> Dict[str, float]:
        """Detect emotional context from user message"""
        emotions = {}
        message_lower = message.lower()
        
        # Stress and anxiety indicators
        stress_words = ['stress', 'stressed', 'overwhelmed', 'pressure', 'deadline', 'urgent', 'panic', 'worried', 'anxiety']
        if any(word in message_lower for word in stress_words):
            emotions['stress'] = 0.7
        
        # Help-seeking indicators
        help_words = ['help', 'assist', 'support', 'guidance', 'advice', 'stuck', 'confused', 'lost']
        if any(word in message_lower for word in help_words):
            emotions['seeking_help'] = 0.6
        
        # Positive emotions
        positive_words = ['happy', 'great', 'awesome', 'excited', 'good', 'excellent', 'wonderful', 'amazing']
        if any(word in message_lower for word in positive_words):
            emotions['positive'] = 0.6
        
        # Negative emotions
        negative_words = ['sad', 'upset', 'angry', 'frustrated', 'disappointed', 'terrible', 'awful']
        if any(word in message_lower for word in negative_words):
            emotions['negative'] = 0.6
        
        # Urgency indicators
        urgency_words = ['urgent', 'asap', 'quickly', 'immediately', 'now', 'emergency']
        if any(word in message_lower for word in urgency_words):
            emotions['urgency'] = 0.8
        
        # Learning/curiosity
        learning_words = ['learn', 'understand', 'explain', 'how', 'what', 'why', 'curious']
        if any(word in message_lower for word in learning_words):
            emotions['curiosity'] = 0.5
        
        return emotions
    
    def _calculate_message_importance(self, message: str, emotional_context: Dict[str, float]) -> float:
        """Calculate importance score for message"""
        base_importance = 0.5
        
        # Increase for emotional content
        if emotional_context:
            max_emotion = max(emotional_context.values())
            base_importance += max_emotion * 0.3
        
        # Increase for message length (more thought)
        if len(message) > 100:
            base_importance += 0.15
        elif len(message) > 200:
            base_importance += 0.25
        
        # Increase for questions
        if '?' in message:
            base_importance += 0.1
        
        # Increase for urgent content
        urgent_words = ['urgent', 'help', 'important', 'critical', 'emergency']
        if any(word in message.lower() for word in urgent_words):
            base_importance += 0.2
        
        return min(base_importance, 1.0)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            user_experiences = self.memory_manager.retrieve_experiences("user", 50)
            consolidated_memories = [exp for exp in user_experiences 
                                   if exp.get('experience', {}).get('type') == 'consolidated_memory']
            
            relationship_network = self.relationship_network.get_relationship_network("user")
            intervention_status = self.autonomous_assistant.get_intervention_status()
            health_summary = self.health_monitor.get_health_summary()
            
            return {
                "system_running": self.running,
                "total_memories": len(user_experiences),
                "consolidated_memories": len(consolidated_memories),
                "patterns_detected": len(consolidated_memories),
                "pattern_confidence": 0.8 if len(consolidated_memories) > 0 else 0.0,
                "total_relationships": relationship_network.get("total_relationships", 0),
                "relationship_health": relationship_network.get("network_health", "developing"),
                "autonomous_mode": intervention_status.get("autonomous_mode", False),
                "proactive_interventions": intervention_status.get("total_interventions", 0),
                "system_health": health_summary.get("overall_health", "healthy"),
                "agents_active": len(self.agent_network.agents)
            }
        except Exception:
            return {
                "system_running": self.running,
                "status": "System monitoring temporarily unavailable"
            }
    
    def run_memory_consolidation(self) -> Dict[str, Any]:
        """Run memory consolidation process"""
        try:
            return self.consolidation_engine.consolidate_memories("user")
        except Exception as e:
            return {"error": str(e), "status": "consolidation_failed"}
    
    def start_interactive_chat(self):
        """Start interactive chat session"""
        print("\n" + "="*60)
        print("🎉 AI Life Operating System - Interactive Chat Mode")
        print("="*60)
        print("💬 Ask me anything! I can help with:")
        print("   • Stress management and emotional support")
        print("   • Task organization and productivity")
        print("   • Communication and relationship advice")  
        print("   • Learning and personal development")
        print("   • General questions and assistance")
        print("\n💡 Type 'status' for system information")
        print("💡 Type 'quit' to exit")
        print("-"*60)
        
        conversation_count = 0
        
        while True:
            try:
                # Get user input
                user_input = input("\n🧑 You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'stop']:
                    print("\n👋 Thank you for using AI Life Operating System!")
                    print("🎯 Session Summary:")
                    print(f"   • {conversation_count} conversations")
                    
                    try:
                        status = self.get_system_status()
                        print(f"   • {status.get('total_memories', 0)} memories stored")
                        print(f"   • {status.get('patterns_detected', 0)} patterns detected")
                        print(f"   • {status.get('total_relationships', 0)} relationships tracked")
                    except:
                        pass
                    
                    print("   • All learning saved for next session")
                    break
                
                if user_input.lower() == 'status':
                    status = self.get_system_status()
                    print(f"\n📊 AI Life OS Status:")
                    print(f"   • System Health: {status.get('system_health', 'Unknown')}")
                    print(f"   • Active Agents: {status.get('agents_active', 0)}")
                    print(f"   • Total Memories: {status.get('total_memories', 0)}")
                    print(f"   • Patterns Detected: {status.get('patterns_detected', 0)}")
                    print(f"   • Relationships: {status.get('total_relationships', 0)}")
                    print(f"   • Autonomous Mode: {'Active' if status.get('autonomous_mode') else 'Inactive'}")
                    print(f"   • Proactive Interventions: {status.get('proactive_interventions', 0)}")
                    continue
                
                if not user_input:
                    print("Please type a message or question...")
                    continue
                
                # Get AI response
                print("🤖 AI Life OS: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                
                conversation_count += 1
                
                # Periodic memory consolidation (every 10 conversations)
                if conversation_count % 10 == 0:
                    print("\n🧠 [Running memory consolidation...]")
                    self.run_memory_consolidation()
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat session ended by user.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again...")
    
    def stop(self):
        """Stop AI Life OS"""
        self.running = False
        try:
            self.event_manager.stop_internal_clock()
            self.health_monitor.stop_monitoring()
        except:
            pass
        print("🛑 AI Life OS stopped")

def main():
    """Main function to start AI Life Operating System"""
    print("🚀 Initializing AI Life Operating System...")
    
    # Create and initialize system
    ai_system = AILifeOperatingSystem()
    
    try:
        if ai_system.initialize():
            # Start interactive chat
            ai_system.start_interactive_chat()
        else:
            print("❌ Failed to initialize AI Life Operating System")
            print("Please check your configuration and try again.")
    
    except KeyboardInterrupt:
        print("\n🛑 System shutdown requested")
    except Exception as e:
        print(f"❌ System error: {e}")
    finally:
        ai_system.stop()

if __name__ == "__main__":
    main()
