from hybrid_agent_manager import HybridAgentManager
from agent_network import AILifeAgentNetwork
from events.event_manager import EventManager
from memory.memory_manager import MemoryManager
import time

class AILifeOperatingSystem:
    def __init__(self):
        self.agent_network = AILifeAgentNetwork()
        self.event_manager = EventManager()
        self.memory_manager = MemoryManager()
        self.running = False
    
    def initialize(self):
        """Initialize the complete AI Life OS"""
        print("🚀 Starting AI Life Operating System...")
        
        # Initialize agent network
        if self.agent_network.initialize_network():
            print("✅ Agent network ready")
        else:
            print("❌ Agent network failed")
            return False
        
        # Start proactive event system
        self.event_manager.start_internal_clock(300)  # 5-minute intervals
        self._setup_event_handlers()
        
        print("✅ AI Life OS fully initialized")
        self.running = True
        return True
    
    def _setup_event_handlers(self):
        """Set up proactive event handling"""
        def handle_periodic_check(event_data):
            print("⏰ Periodic system check triggered")
            # Trigger orchestrator periodic check
            orchestrator = self.agent_network.orchestrator
            if orchestrator:
                result = orchestrator.process_periodic_check()
                print(f"📊 System health: {result.get('system_health')}")
        
        # Subscribe to internal clock events
        event_handler = self.event_manager.subscribe_to_events(handle_periodic_check)
        
        # Start event listener in background
        import threading
        listener_thread = threading.Thread(target=event_handler)
        listener_thread.daemon = True
        listener_thread.start()
    
    def chat(self, message: str, agent_name: str = None) -> str:
        """Main chat interface"""
        if not self.running:
            return "System not initialized. Call initialize() first."
        
        # Store user message in memory
        self.memory_manager.store_experience(
            "user", 
            {"type": "chat", "message": message},
            {"engagement": "active"}
        )
        
        # Route to appropriate agent
        response = self.agent_network.route_message(message, agent_name)
        
        # Store response in memory
        self.memory_manager.store_experience(
            "system",
            {"type": "response", "message": response.get('response', '')},
            {"success": True}
        )
        
        return response.get('response', 'No response generated')
    
    def get_status(self):
        """Get complete system status"""
        return {
            "system_running": self.running,
            "network_status": self.agent_network.get_network_status(),
            "memory_entries": len(self.memory_manager.retrieve_experiences("user")),
            "uptime": time.time()
        }

# Simple usage example
if __name__ == "__main__":
    # Create and start the system
    ai_system = AILifeOperatingSystem()
    
    if ai_system.initialize():
        print("\n🎉 AI Life OS Ready!")
        
        # Test interactions
        print("\n💬 Testing chat interface...")
        
        response1 = ai_system.chat("Hello! What's your name and what can you do?")
        print(f"AI: {response1}")
        
        response2 = ai_system.chat("I'm feeling stressed about work. Can you help?")
        print(f"AI: {response2}")
        
        response3 = ai_system.chat("What should I do if I don't reply to a message for 5 minutes?")
        print(f"AI: {response3}")
        
        # Show status
        status = ai_system.get_status()
        print(f"\n📊 System Status: {status['network_status']['network_size']} agents active")
    
    else:
        print("❌ System initialization failed")
