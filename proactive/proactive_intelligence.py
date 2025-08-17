"""
Proactive Intelligence Engine for AI Life Operating System
Provides advanced prediction, autonomous planning, and anticipatory capabilities
"""


import time
from typing import Dict, Any, List, Optional
from memory.pattern_recognition import PatternRecognitionEngine
from memory.memory_consolidation import MemoryConsolidationEngine


class ProactiveIntelligenceEngine:
    def __init__(self, memory_manager=None, pattern_engine=None, consolidation_engine=None):
        self.memory_manager = memory_manager
        self.pattern_engine = pattern_engine or PatternRecognitionEngine(memory_manager)
        self.consolidation_engine = consolidation_engine or MemoryConsolidationEngine(memory_manager)
        self.proactive_tasks = []  # Queue of planned proactive actions
        self.prediction_history = []
        self.intervention_threshold = 0.7
        print("⚡ Proactive Intelligence Engine initialized")


    def analyze_and_predict(self, user_id: str) -> Dict[str, Any]:
        """Analyze patterns and predict user needs proactively"""
        try:
            # Get comprehensive analysis
            pattern_data = self.pattern_engine.analyze_all_patterns(user_id)
            consolidated_data = self.consolidation_engine.get_consolidated_insights(user_id)
            predictions = self.pattern_engine.predict_user_needs(user_id)


            # Generate proactive plan
            proactive_plan = self._generate_proactive_plan(pattern_data, predictions)
            
            # Store prediction for learning
            self.prediction_history.append({
                "timestamp": time.time(),
                "predictions": predictions,
                "confidence": self._calculate_overall_confidence(predictions)
            })


            return {
                "user_id": user_id,
                "timestamp": time.time(),
                "pattern_analysis": pattern_data,
                "memory_consolidation": consolidated_data,
                "predictions": predictions,
                "proactive_plan": proactive_plan,
                "overall_confidence": self._calculate_overall_confidence(predictions)
            }


        except Exception as e:
            print(f"⚠️ Proactive analysis failed: {e}")
            return {
                "user_id": user_id,
                "error": str(e),
                "proactive_plan": [],
                "overall_confidence": 0.0
            }


    def _generate_proactive_plan(self, pattern_data: Dict[str, Any], predictions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fixed proactive plan generation with lower thresholds"""
        tasks = []
        current_time = time.time()
        
        print(f"🔮 Generating plan from {len(predictions.get('predictions', []))} predictions...")
        
        # Process predictions with LOWER threshold (0.5 instead of 0.7)
        for prediction in predictions.get("predictions", []):
            predicted_need = prediction.get("predicted_need", "general_assistance")
            confidence = prediction.get("confidence", 0.5)
            
            # LOWER threshold to allow more predictions through
            if confidence >= 0.5:  # Changed from 0.7 to 0.5
                task = {
                    "id": f"proactive_{int(current_time)}_{len(tasks)}",
                    "type": "proactive_intervention",
                    "category": predicted_need,
                    "confidence": confidence,
                    "priority": self._determine_priority(confidence, predicted_need),
                    "description": self._generate_task_description(predicted_need, confidence),
                    "reasoning": prediction.get("reasoning", "Pattern-based prediction"),
                    "suggested_actions": prediction.get("suggested_actions", []),
                    "timestamp": current_time
                }
                tasks.append(task)
                print(f"✅ Added task: {predicted_need} (confidence: {confidence:.2f})")
            else:
                print(f"⚠️ Skipped low confidence prediction: {predicted_need} ({confidence:.2f})")
        
        # Add pattern-based tasks even if no predictions
        if not tasks and pattern_data.get('confidence_score', 0) > 0.5:
            # Create a general proactive task based on patterns
            tasks.append({
                "id": f"pattern_general_{int(current_time)}",
                "type": "pattern_based_assistance",
                "category": "general_support",
                "confidence": pattern_data.get('confidence_score', 0.6),
                "priority": "medium",
                "description": "Provide general assistance based on detected patterns",
                "reasoning": "Strong patterns detected, offering general support",
                "timestamp": current_time
            })
            print(f"✅ Added fallback pattern-based task")
        
        print(f"🎯 Generated {len(tasks)} proactive tasks")
        return tasks


    def _determine_priority(self, confidence: float, predicted_need: str) -> str:
        """Determine task priority based on confidence and need type"""
        high_priority_needs = ["stress_management_support", "immediate_stress_relief", "urgent_assistance"]
        
        if confidence > 0.9 or predicted_need in high_priority_needs:
            return "urgent"
        elif confidence > 0.8:
            return "high"
        elif confidence > 0.7:
            return "medium"
        else:
            return "low"


    def _priority_score(self, priority: str) -> int:
        """Convert priority to numeric score for sorting"""
        scores = {"urgent": 4, "high": 3, "medium": 2, "low": 1}
        return scores.get(priority, 1)


    def _generate_task_description(self, predicted_need: str, confidence: float) -> str:
        """Generate human-readable task description"""
        descriptions = {
            "stress_management_support": f"Provide stress management assistance (confidence: {confidence:.1%})",
            "assistance_with_work": f"Offer work-related productivity support (confidence: {confidence:.1%})",
            "learning_support": f"Provide learning optimization guidance (confidence: {confidence:.1%})",
            "productivity_optimization": f"Suggest productivity improvements (confidence: {confidence:.1%})",
            "emotional_support": f"Offer emotional wellness support (confidence: {confidence:.1%})"
        }
        
        return descriptions.get(
            predicted_need, 
            f"Provide proactive assistance with {predicted_need.replace('_', ' ')} (confidence: {confidence:.1%})"
        )


    def _calculate_execution_window(self, predicted_need: str) -> Dict[str, float]:
        """Calculate optimal execution timing for task"""
        # Immediate needs
        immediate_needs = ["immediate_stress_relief", "urgent_assistance"]
        if predicted_need in immediate_needs:
            return {"start": time.time(), "end": time.time() + 300}  # 5 minutes
        
        # High-impact needs
        high_impact_needs = ["stress_management_support", "productivity_optimization"]
        if predicted_need in high_impact_needs:
            return {"start": time.time() + 600, "end": time.time() + 1800}  # 10-30 minutes
        
        # General needs
        return {"start": time.time() + 1800, "end": time.time() + 3600}  # 30-60 minutes


    def _estimate_task_impact(self, predicted_need: str, confidence: float) -> float:
        """Estimate potential positive impact of task"""
        impact_scores = {
            "stress_management_support": 0.9,
            "immediate_stress_relief": 0.95,
            "productivity_optimization": 0.8,
            "learning_support": 0.7,
            "assistance_with_work": 0.85
        }
        
        base_impact = impact_scores.get(predicted_need, 0.6)
        return min(1.0, base_impact * confidence)


    def _generate_pattern_based_tasks(self, pattern_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate additional tasks based on pattern analysis"""
        tasks = []
        patterns = pattern_data.get("actionable_insights", [])
        
        for insight in patterns[:3]:  # Limit to top 3 insights
            if "stress" in insight.lower():
                tasks.append({
                    "id": f"pattern_stress_{int(time.time())}",
                    "type": "pattern_intervention",
                    "category": "stress_pattern_support",
                    "confidence": 0.8,
                    "priority": "medium",
                    "description": "Address recurring stress pattern",
                    "reasoning": insight,
                    "timestamp": time.time(),
                    "pattern_based": True
                })
            elif "proactive" in insight.lower():
                tasks.append({
                    "id": f"pattern_proactive_{int(time.time())}",
                    "type": "pattern_enhancement",
                    "category": "proactive_assistance",
                    "confidence": 0.75,
                    "priority": "medium", 
                    "description": "Enhance proactive assistance",
                    "reasoning": insight,
                    "timestamp": time.time(),
                    "pattern_based": True
                })
        
        return tasks


    def _calculate_overall_confidence(self, predictions: Dict[str, Any]) -> float:
        """Calculate overall confidence in predictions"""
        prediction_list = predictions.get("predictions", [])
        if not prediction_list:
            return 0.0
        
        confidences = [p.get("confidence", 0.5) for p in prediction_list]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Boost confidence if multiple high-confidence predictions
        high_conf_count = sum(1 for c in confidences if c > 0.8)
        confidence_boost = min(0.2, (high_conf_count / len(confidences)) * 0.2)
        
        return min(1.0, avg_confidence + confidence_boost)


    def execute_proactive_tasks(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Execute queued proactive tasks"""
        executed_tasks = []
        current_time = time.time()
        
        # Filter tasks ready for execution
        ready_tasks = [
            task for task in self.proactive_tasks 
            if self._is_task_ready(task, current_time)
        ]
        
        # Execute up to limit number of tasks
        for task in ready_tasks[:limit]:
            try:
                result = self._execute_single_task(task)
                task["execution_result"] = result
                task["executed_at"] = current_time
                task["status"] = "completed"
                
                executed_tasks.append(task)
                print(f"🛎️ Executed: {task['description']}")
                
            except Exception as e:
                task["execution_result"] = {"error": str(e)}
                task["executed_at"] = current_time
                task["status"] = "failed"
                print(f"❌ Task execution failed: {e}")
        
        # Remove executed tasks from queue
        self.proactive_tasks = [
            task for task in self.proactive_tasks 
            if task.get("status") not in ["completed", "failed"]
        ]
        
        return executed_tasks


    def _is_task_ready(self, task: Dict[str, Any], current_time: float) -> bool:
        """Check if task is ready for execution"""
        execution_window = task.get("execution_window", {})
        start_time = execution_window.get("start", current_time)
        end_time = execution_window.get("end", current_time + 3600)
        
        return start_time <= current_time <= end_time


    def _execute_single_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single proactive task"""
        category = task.get("category", "general")
        
        # Simulate task execution (in real system, this would trigger agents)
        execution_results = {
            "stress_management_support": "Stress management resources prepared and delivered",
            "productivity_optimization": "Productivity suggestions generated and queued",
            "learning_support": "Learning optimization tips prepared",
            "immediate_stress_relief": "Quick stress relief technique provided"
        }
        
        result_message = execution_results.get(category, f"Proactive assistance for {category} prepared")
        
        return {
            "task_id": task.get("id"),
            "category": category,
            "result": result_message,
            "impact_score": task.get("estimated_impact", 0.5),
            "success": True
        }


    def plan_next_actions(self, user_id: str) -> Dict[str, Any]:
        """Main method: analyze, predict, and plan proactive actions"""
        print(f"🔮 Planning proactive actions for {user_id}...")
        
        # Run comprehensive analysis
        analysis = self.analyze_and_predict(user_id)
        
        # Add planned tasks to queue
        new_tasks = analysis.get("proactive_plan", [])
        self.proactive_tasks.extend(new_tasks)
        
        # Remove duplicate or outdated tasks
        self._cleanup_task_queue()
        
        planning_summary = {
            "analysis": analysis,
            "new_tasks_planned": len(new_tasks),
            "total_queued_tasks": len(self.proactive_tasks),
            "high_priority_tasks": len([t for t in self.proactive_tasks if t.get("priority") in ["urgent", "high"]]),
            "planning_confidence": analysis.get("overall_confidence", 0.0)
        }
        
        print(f"✅ Planned {len(new_tasks)} new proactive tasks (confidence: {analysis.get('overall_confidence', 0):.1%})")
        
        return planning_summary


    def _cleanup_task_queue(self):
        """Remove duplicate and outdated tasks"""
        current_time = time.time()
        
        # Remove expired tasks
        self.proactive_tasks = [
            task for task in self.proactive_tasks
            if task.get("execution_window", {}).get("end", current_time + 3600) > current_time
        ]
        
        # Remove duplicates based on category
        seen_categories = set()
        unique_tasks = []
        
        for task in self.proactive_tasks:
            category = task.get("category", "unknown")
            if category not in seen_categories:
                unique_tasks.append(task)
                seen_categories.add(category)
        
        self.proactive_tasks = unique_tasks


    def get_proactive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of proactive intelligence"""
        return {
            "queued_tasks": len(self.proactive_tasks),
            "prediction_history_count": len(self.prediction_history),
            "intervention_threshold": self.intervention_threshold,
            "recent_confidence": self.prediction_history[-1].get("confidence", 0.0) if self.prediction_history else 0.0,
            "high_priority_tasks": len([t for t in self.proactive_tasks if t.get("priority") in ["urgent", "high"]]),
            "ready_for_execution": len([t for t in self.proactive_tasks if self._is_task_ready(t, time.time())]),
            "system_health": "optimal" if len(self.proactive_tasks) > 0 else "ready"
        }


# Test Proactive Intelligence Engine
if __name__ == "__main__":
    print("🧪 Testing Proactive Intelligence Engine...")


    from memory.memory_manager import MemoryManager


    memory_manager = MemoryManager()
    pattern_engine = PatternRecognitionEngine(memory_manager)
    consolidation_engine = MemoryConsolidationEngine(memory_manager)


    proactive_engine = ProactiveIntelligenceEngine(memory_manager, pattern_engine, consolidation_engine)


    # Test planning
    planning_result = proactive_engine.plan_next_actions("test_user")
    print(f"✅ Planning result: {planning_result['new_tasks_planned']} tasks planned")


    # Test execution
    executed_tasks = proactive_engine.execute_proactive_tasks()
    print(f"✅ Executed {len(executed_tasks)} proactive tasks")


    # Test status
    status = proactive_engine.get_proactive_status()
    print(f"✅ System status: {status['system_health']} ({status['queued_tasks']} queued)")


    print("🎉 Proactive Intelligence Engine test complete!")
