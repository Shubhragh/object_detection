"""
Autonomous Assistant Manager for AI Life Operating System
Manages autonomous operations and proactive interventions
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import threading

class AutonomousAssistantManager:
    """Manages autonomous AI operations and proactive assistance"""
    
    def __init__(self, agent_network=None, memory_manager=None):
        self.agent_network = agent_network
        self.memory_manager = memory_manager
        self.autonomous_mode = False
        self.active_interventions = []
        self.intervention_history = []
        
        # Autonomous operation parameters
        self.intervention_cooldown = 300  # 5 minutes between interventions
        self.max_concurrent_interventions = 3
        self.autonomous_confidence_threshold = 0.8
        
        print("🤖 Autonomous Assistant Manager initialized")
    
    def enable_autonomous_mode(self):
        """Enable autonomous proactive assistance"""
        self.autonomous_mode = True
        print("🔄 Autonomous mode ENABLED - AI will proactively assist")
    
    def disable_autonomous_mode(self):
        """Disable autonomous mode"""
        self.autonomous_mode = False
        print("⏸️ Autonomous mode DISABLED")
    
    def execute_proactive_intervention(self, intervention: Dict[str, Any], user_id: str = "user") -> Dict[str, Any]:
        """Execute a proactive intervention"""
        if not self.autonomous_mode:
            return {"status": "skipped", "reason": "Autonomous mode disabled"}
        
        if len(self.active_interventions) >= self.max_concurrent_interventions:
            return {"status": "deferred", "reason": "Too many active interventions"}
        
        # Check cooldown period
        if self._is_in_cooldown():
            return {"status": "deferred", "reason": "Intervention cooldown active"}
        
        intervention_id = f"intervention_{int(time.time())}"
        intervention["id"] = intervention_id
        intervention["started_at"] = time.time()
        intervention["status"] = "executing"
        
        self.active_interventions.append(intervention)
        
        try:
            # Execute the intervention based on type
            result = self._execute_intervention_by_type(intervention, user_id)
            
            intervention["status"] = "completed"
            intervention["completed_at"] = time.time()
            intervention["result"] = result
            
            # Move to history
            self.intervention_history.append(intervention)
            self.active_interventions = [i for i in self.active_interventions if i["id"] != intervention_id]
            
            print(f"✅ Proactive intervention completed: {intervention.get('category', 'unknown')}")
            return {"status": "completed", "result": result, "intervention_id": intervention_id}
            
        except Exception as e:
            intervention["status"] = "failed"
            intervention["error"] = str(e)
            intervention["completed_at"] = time.time()
            
            self.intervention_history.append(intervention)
            self.active_interventions = [i for i in self.active_interventions if i["id"] != intervention_id]
            
            print(f"❌ Proactive intervention failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _execute_intervention_by_type(self, intervention: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Execute intervention based on its type"""
        category = intervention.get('category', 'general')
        
        if category == 'stress_management_support':
            return self._provide_stress_management(intervention, user_id)
        elif category == 'productivity_optimization':
            return self._provide_productivity_assistance(intervention, user_id)
        elif category == 'immediate_stress_relief':
            return self._provide_immediate_stress_relief(intervention, user_id)
        elif category == 'learning_support':
            return self._provide_learning_support(intervention, user_id)
        else:
            return self._provide_general_assistance(intervention, user_id)
    
    def _provide_stress_management(self, intervention: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide proactive stress management assistance"""
        if self.agent_network and hasattr(self.agent_network, 'orchestrator'):
            # Route to stress management agent
            stress_message = f"""
PROACTIVE STRESS MANAGEMENT INTERVENTION:
Based on pattern analysis, the user may benefit from stress management support.

Reasoning: {intervention.get('reasoning', 'Pattern-based prediction')}
Confidence: {intervention.get('confidence', 0.5):.1%}

Please provide:
1. Brief stress assessment
2. Immediate stress relief technique
3. Long-term stress management suggestion
4. Gentle check-in question

Keep response supportive and non-intrusive.
"""
            
            try:
                response = self.agent_network.orchestrator.route_message(stress_message, "stressmanagementagent")
                
                # Store the proactive intervention
                if self.memory_manager:
                    self.memory_manager.store_enhanced_experience(
                        user_id,
                        {
                            "type": "proactive_intervention",
                            "category": "stress_management", 
                            "intervention_data": intervention,
                            "response": response.get('response', '')
                        },
                        {"proactive_assistance": 1.0, "stress_support": 0.8},
                        0.9
                    )
                
                return {
                    "type": "stress_management",
                    "response": response.get('response', 'Stress management assistance provided'),
                    "agent_used": "StressManagementAgent",
                    "success": True
                }
                
            except Exception as e:
                return {"type": "stress_management", "error": str(e), "success": False}
        
        return {"type": "stress_management", "message": "Stress management resources prepared", "success": True}
    
    def _provide_productivity_assistance(self, intervention: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide proactive productivity assistance"""
        if self.agent_network and hasattr(self.agent_network, 'orchestrator'):
            productivity_message = f"""
PROACTIVE PRODUCTIVITY OPTIMIZATION:
Pattern analysis suggests the user could benefit from productivity assistance.

Reasoning: {intervention.get('reasoning', 'Temporal pattern analysis')}

Please provide:
1. Time management tip relevant to current time
2. Task prioritization suggestion
3. Quick productivity boost technique
4. Optional check-in about current workload

Keep response helpful but optional for user to engage with.
"""
            
            try:
                response = self.agent_network.orchestrator.route_message(productivity_message, "productivityagent")
                
                if self.memory_manager:
                    self.memory_manager.store_enhanced_experience(
                        user_id,
                        {
                            "type": "proactive_intervention",
                            "category": "productivity_optimization",
                            "intervention_data": intervention,
                            "response": response.get('response', '')
                        },
                        {"proactive_assistance": 1.0, "productivity_support": 0.8},
                        0.8
                    )
                
                return {
                    "type": "productivity_optimization", 
                    "response": response.get('response', 'Productivity assistance provided'),
                    "agent_used": "ProductivityAgent",
                    "success": True
                }
                
            except Exception as e:
                return {"type": "productivity_optimization", "error": str(e), "success": False}
        
        return {"type": "productivity_optimization", "message": "Productivity tips prepared", "success": True}
    
    def _provide_immediate_stress_relief(self, intervention: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide immediate stress relief intervention"""
        relief_techniques = [
            "Take 3 deep breaths: inhale for 4 counts, hold for 4, exhale for 6",
            "Progressive muscle relaxation: tense and release your shoulders for 5 seconds",
            "5-4-3-2-1 grounding: name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste",
            "Quick walk or stretch break to reset your energy"
        ]
        
        selected_technique = relief_techniques[int(time.time()) % len(relief_techniques)]
        
        if self.memory_manager:
            self.memory_manager.store_enhanced_experience(
                user_id,
                {
                    "type": "proactive_intervention",
                    "category": "immediate_stress_relief",
                    "technique_provided": selected_technique,
                    "intervention_data": intervention
                },
                {"immediate_support": 1.0, "stress_relief": 0.9},
                0.85
            )
        
        return {
            "type": "immediate_stress_relief",
            "technique": selected_technique,
            "message": f"Quick stress relief suggestion: {selected_technique}",
            "success": True
        }
    
    def _provide_learning_support(self, intervention: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide proactive learning support"""
        if self.agent_network and hasattr(self.agent_network, 'orchestrator'):
            learning_message = f"""
PROACTIVE LEARNING SUPPORT:
User shows high question frequency, suggesting active learning mode.

Please provide:
1. Learning optimization tip
2. Study technique recommendation  
3. Knowledge retention strategy
4. Offer to help with any current learning goals

Make response encouraging and supportive of their learning journey.
"""
            
            try:
                response = self.agent_network.orchestrator.route_message(learning_message, "contextagent")
                
                if self.memory_manager:
                    self.memory_manager.store_enhanced_experience(
                        user_id,
                        {
                            "type": "proactive_intervention",
                            "category": "learning_support",
                            "intervention_data": intervention,
                            "response": response.get('response', '')
                        },
                        {"proactive_assistance": 1.0, "learning_support": 0.7},
                        0.75
                    )
                
                return {
                    "type": "learning_support",
                    "response": response.get('response', 'Learning support provided'),
                    "agent_used": "ContextAgent",
                    "success": True
                }
                
            except Exception as e:
                return {"type": "learning_support", "error": str(e), "success": False}
        
        return {"type": "learning_support", "message": "Learning resources prepared", "success": True}
    
    def _provide_general_assistance(self, intervention: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Provide general proactive assistance"""
        return {
            "type": "general_assistance",
            "message": f"Proactive assistance: {intervention.get('description', 'General support available')}",
            "success": True
        }
    
    def _is_in_cooldown(self) -> bool:
        """Check if we're in cooldown period"""
        if not self.intervention_history:
            return False
        
        last_intervention = max(self.intervention_history, key=lambda x: x.get('completed_at', 0))
        time_since_last = time.time() - last_intervention.get('completed_at', 0)
        
        return time_since_last < self.intervention_cooldown
    
    def get_intervention_status(self) -> Dict[str, Any]:
        """Get status of autonomous interventions"""
        return {
            "autonomous_mode": self.autonomous_mode,
            "active_interventions": len(self.active_interventions),
            "total_interventions": len(self.intervention_history),
            "last_intervention": self.intervention_history[-1] if self.intervention_history else None,
            "success_rate": self._calculate_success_rate(),
            "cooldown_active": self._is_in_cooldown()
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate intervention success rate"""
        if not self.intervention_history:
            return 1.0
        
        successful = sum(1 for i in self.intervention_history if i.get('status') == 'completed')
        return successful / len(self.intervention_history)

# Test autonomous assistant
if __name__ == "__main__":
    print("🧪 Testing Autonomous Assistant Manager...")
    
    assistant = AutonomousAssistantManager()
    assistant.enable_autonomous_mode()
    
    # Test intervention
    test_intervention = {
        "category": "immediate_stress_relief",
        "description": "Provide immediate stress relief",
        "confidence": 0.85,
        "reasoning": "High stress indicators detected"
    }
    
    result = assistant.execute_proactive_intervention(test_intervention)
    print(f"✅ Intervention result: {result['status']}")
    
    status = assistant.get_intervention_status()
    print(f"✅ Intervention status: {status['success_rate']:.1%} success rate")
    
    print("🎉 Autonomous Assistant Manager test complete!")
