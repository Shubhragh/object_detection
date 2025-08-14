import sys
import time
import asyncio
from setup_database import setup_postgres, setup_redis
from letta_manager import LettaManager
from agents.orchestrator_agent import OrchestratorAgent
from events.event_manager import EventManager
from memory.memory_manager import MemoryManager

class SystemIntegrationTest:
    def __init__(self):
        self.results = {}
        
    def test_database_setup(self):
        """Test database connectivity"""
        print("🧪 Testing database setup...")
        try:
            # Test PostgreSQL
            asyncio.run(setup_postgres())
            
            # Test Redis
            redis_client = setup_redis()
            if redis_client:
                self.results["database"] = "✅ PASS"
                return True
            else:
                self.results["database"] = "❌ FAIL"
                return False
        except Exception as e:
            print(f"Database test failed: {e}")
            self.results["database"] = "❌ FAIL"
            return False
    
    def test_letta_manager(self):
        """Test Letta integration"""
        print("🧪 Testing Letta manager...")
        try:
            letta = LettaManager()
            
            # Create test agent
            agent = letta.create_agent(
                name="SystemTestAgent",
                system_prompt="You are a test agent. Respond briefly to confirm you're working."
            )
            
            if agent and agent.get('id'):
                # Test message sending
                response = letta.send_message(agent['id'], "Are you working properly?")
                if response:
                    self.results["letta"] = "✅ PASS"
                    return True
            
            self.results["letta"] = "❌ FAIL"
            return False
        except Exception as e:
            print(f"Letta test failed: {e}")
            self.results["letta"] = "❌ FAIL"
            return False
    
    def test_orchestrator_agent(self):
        """Test orchestrator agent"""
        print("🧪 Testing orchestrator agent...")
        try:
            orchestrator = OrchestratorAgent()
            if orchestrator.initialize():
                # Test query tracking
                orchestrator.track_query("test_query", "What is your name?")
                
                # Test timeout checking (with very short timeout for testing)
                time.sleep(1)
                timeouts = orchestrator.check_timeouts(0)  # Immediate timeout for testing
                
                if len(timeouts) > 0:
                    self.results["orchestrator"] = "✅ PASS"
                    return True
            
            self.results["orchestrator"] = "❌ FAIL"
            return False
        except Exception as e:
            print(f"Orchestrator test failed: {e}")
            self.results["orchestrator"] = "❌ FAIL"
            return False
    
    def test_event_system(self):
        """Test event management"""
        print("🧪 Testing event system...")
        try:
            event_manager = EventManager()
            
            # Test event publishing
            success = event_manager.publish_event(
                "test_event",
                {"message": "System test event"},
                "system_test"
            )
            
            if success:
                self.results["events"] = "✅ PASS"
                return True
            else:
                self.results["events"] = "❌ FAIL"
                return False
        except Exception as e:
            print(f"Event system test failed: {e}")
            self.results["events"] = "❌ FAIL"
            return False
    
    def test_memory_system(self):
        """Test memory management"""
        print("🧪 Testing memory system...")
        try:
            memory = MemoryManager()
            
            # Test experience storage
            test_exp = {"test": "memory storage"}
            success = memory.store_experience("test_user", test_exp)
            
            if success:
                # Test retrieval
                experiences = memory.retrieve_experiences("test_user", 1)
                if len(experiences) > 0:
                    self.results["memory"] = "✅ PASS"
                    return True
            
            self.results["memory"] = "❌ FAIL"
            return False
        except Exception as e:
            print(f"Memory system test failed: {e}")
            self.results["memory"] = "❌ FAIL"
            return False
    
    def run_all_tests(self):
        """Run complete system integration test"""
        print("🚀 Starting System Integration Test")
        print("="*50)
        
        tests = [
            self.test_database_setup,
            self.test_letta_manager,
            self.test_orchestrator_agent,
            self.test_event_system,
            self.test_memory_system
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"Test failed with exception: {e}")
        
        print("\n" + "="*50)
        print("📊 TEST RESULTS:")
        for component, result in self.results.items():
            print(f"{component:15}: {result}")
        
        all_passed = all("✅" in result for result in self.results.values())
        if all_passed:
            print("\n🎉 ALL TESTS PASSED! System ready for Step 2.")
        else:
            print("\n⚠️  Some tests failed. Please fix issues before proceeding.")
        
        return all_passed

if __name__ == "__main__":
    tester = SystemIntegrationTest()
    tester.run_all_tests()
