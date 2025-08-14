from ai_life_system import AILifeOperatingSystem
import time

def test_scenario_suite():
    """Test real-world usage scenarios"""
    
    scenarios = [
        {
            "name": "Morning Productivity Assistant",
            "messages": [
                "Good morning! I have a busy day ahead and need help organizing my priorities.",
                "I have 3 meetings, 2 deadlines, and some personal errands. What should I focus on first?",
                "Actually, I'm feeling a bit overwhelmed. Can you help me break this down?"
            ]
        },
        {
            "name": "Stress Management Support", 
            "messages": [
                "I'm feeling really stressed about my workload lately.",
                "I keep forgetting important tasks and it's making things worse.",
                "What strategies do you recommend for managing stress and staying organized?"
            ]
        },
        {
            "name": "Social Communication Help",
            "messages": [
                "I need to write a difficult email to my boss about a project delay.",
                "I want to be professional but also explain the circumstances clearly.",
                "Can you help me draft something appropriate?"
            ]
        },
        {
            "name": "Learning and Memory Test",
            "messages": [
                "I told you yesterday that I prefer morning workouts. Do you remember that?",
                "Based on what you know about me, what time would be best for scheduling calls?",
                "Can you remind me what we discussed about my goals last week?"
            ]
        },
        {
            "name": "Proactive Assistance Test",
            "messages": [
                "What happens if I don't respond to you for several minutes?",
                "How does your timeout detection work?",
                # Then we'll simulate not responding
            ]
        }
    ]
    
    print("🎬 Starting Real-World Scenario Testing")
    print("="*60)
    
    ai_system = AILifeOperatingSystem()
    if not ai_system.initialize():
        print("❌ System initialization failed")
        return
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎭 Scenario {i}: {scenario['name']}")
        print("-" * 50)
        
        for j, message in enumerate(scenario['messages'], 1):
            print(f"\n👤 User (Step {j}): {message}")
            
            if scenario['name'] == "Proactive Assistance Test" and j == len(scenario['messages']):
                # Special case: test timeout
                orchestrator = ai_system.agent_network.orchestrator
                if orchestrator:
                    query_id = f"scenario_test_{i}_{j}"
                    orchestrator.track_query(query_id, message, "scenario_user")
                    print("⏰ Simulating 5-minute silence...")
                    time.sleep(2)  # Short wait for demo
                    timeouts = orchestrator.check_timeouts(1)  # 1 second timeout for demo
                    if timeouts:
                        result = orchestrator.initiate_escalation(timeouts[0]['id'])
                        print(f"🚨 Proactive Response: {result.get('escalation_response', 'No escalation')[:200]}...")
                    else:
                        print("❌ No proactive response generated")
            else:
                response = ai_system.chat(message)
                print(f"🤖 AI: {response}")
            
            # Brief pause between messages for realism
            time.sleep(0.5)
        
        print(f"\n✅ Scenario {i} completed")
        
        # Ask user if they want to continue
        if i < len(scenarios):
            continue_test = input(f"\nContinue to next scenario? (y/n): ").strip().lower()
            if continue_test != 'y':
                break
    
    print("\n🎉 Scenario testing completed!")

if __name__ == "__main__":
    test_scenario_suite()
