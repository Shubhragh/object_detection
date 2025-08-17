"""
AI Life Operating System - CORRECTED Production Version
Fixed agent management, routing, and response generation
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


# REMOVED: Individual agent imports - let orchestrator manage them
# from agents.emotional_analysis_agent import EmotionalAnalysisAgent
# from agents.intent_classification_agent import IntentClassificationAgent


import time
import threading
from typing import Dict, Any


class AILifeOperatingSystem:
    def __init__(self):
        """Initialize AI Life Operating System with proper agent coordination"""
        
        # Core systems
        self.agent_network = AILifeAgentNetwork()
        self.event_manager = EventManager()


        # Memory system with intelligence
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


        # REMOVED: Individual specialized analysis agents
        # These will be managed by the agent network orchestrator
        
        self.running = False
        print("🤖 AI Life Operating System initialized with centralized agent management")


    def initialize(self) -> bool:
        """Initialize all AI Life OS components with proper agent coordination"""
        print("🚀 Starting AI Life Operating System...")
        # Initialize agent network first
        if not self.agent_network.initialize_network():
            print("❌ Agent network initialization failed")
            return False
        # IMPORTANT: The orchestrator now includes the humanizer automatically
        # No additional changes needed - the enhanced orchestrator handles it
        # Rest of initialization remains the same...

        # FIXED: Let orchestrator manage specialized agents internally
        # No separate agent initialization needed here
        
        # Initialize autonomous assistant with agent network
        self.autonomous_assistant = AutonomousAssistantManager(
            self.agent_network,
            self.memory_manager
        )


        # Start background systems
        self._start_background_systems()


        print("✅ AI Life OS fully operational with centralized agent coordination")
        self.running = True
        return True


    def chat(self, message: str) -> str:
        """COMPLETELY REWRITTEN: Clean, AI-driven response generation"""
        if not self.running:
            return "AI Life OS not initialized. Please restart the system."


        # Check performance cache first
        cached_response = self.performance_optimizer.get_cached_response(message)
        if cached_response:
            return cached_response


        start_time = time.time()


        try:
            print(f"📥 Processing: '{message[:50]}{'...' if len(message) > 50 else ''}'")


            # SINGLE ROUTING DECISION: Let orchestrator handle everything
            routing_result = self.agent_network.orchestrator.route_message(message)
            
            if routing_result.get("routing_success"):
                # Use orchestrator's routing decision
                routed_agent = routing_result.get('routed_to')
                actual_response = routing_result.get('agent_response', routing_result.get('response', ''))
                
                print(f"✅ Successfully routed to: {routed_agent}")
                
            else:
                # Fallback: Use orchestrator's analysis response
                actual_response = routing_result.get('response', 'I apologize, but I was unable to process your request at this time.')
                print("⚠️ Using orchestrator analysis as response")


            # Store interaction in memory (simplified)
            try:
                self.memory_manager.store_experience(
                    "user",
                    {
                        "type": "user_message",
                        "message": message,
                        "response": actual_response,
                        "routed_to": routing_result.get('routed_to', 'orchestrator')
                    },
                    {},  # Let memory manager handle emotional analysis internally
                    0.6
                )
            except Exception as e:
                print(f"⚠️ Memory storage failed: {e}")


            # Update relationship network
            try:
                self.relationship_network.update_relationship_from_interaction(
                    "user", message, {}
                )
            except Exception as e:
                print(f"⚠️ Relationship update failed: {e}")


            # Cache and track performance
            response_time = time.time() - start_time
            self.performance_optimizer.optimize_response_caching(message, actual_response)
            self.performance_optimizer.metrics["response_times"].append(response_time)


            print(f"📤 Response generated in {response_time:.2f}s")
            return actual_response


        except Exception as e:
            print(f"❌ Chat processing failed: {e}")
            return f"I encountered an error processing your request. Please try again."


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
                "agents_active": len(self.agent_network.agents) if hasattr(self.agent_network, 'agents') else 0
            }


        except Exception:
            return {
                "system_running": self.running,
                "status": "System monitoring temporarily unavailable"
            }


    # Keep existing methods: run_memory_consolidation, start_interactive_chat, stop
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
        print(" • Stress management and emotional support")
        print(" • Task organization and productivity")
        print(" • Communication and relationship advice")
        print(" • Learning and personal development")
        print(" • General questions and assistance")
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
                    print(f" • {conversation_count} conversations")
                    try:
                        status = self.get_system_status()
                        print(f" • {status.get('total_memories', 0)} memories stored")
                        print(f" • {status.get('patterns_detected', 0)} patterns detected")
                        print(f" • {status.get('total_relationships', 0)} relationships tracked")
                    except:
                        pass
                    print(" • All learning saved for next session")
                    break


                if user_input.lower() == 'status':
                    status = self.get_system_status()
                    print(f"\n📊 AI Life OS Status:")
                    print(f" • System Health: {status.get('system_health', 'Unknown')}")
                    print(f" • Active Agents: {status.get('agents_active', 0)}")
                    print(f" • Total Memories: {status.get('total_memories', 0)}")
                    print(f" • Patterns Detected: {status.get('patterns_detected', 0)}")
                    print(f" • Relationships: {status.get('total_relationships', 0)}")
                    print(f" • Autonomous Mode: {'Active' if status.get('autonomous_mode') else 'Inactive'}")
                    print(f" • Proactive Interventions: {status.get('proactive_interventions', 0)}")
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
