"""
Predictive Task Planner for AI Life Operating System
Advanced prediction algorithms and autonomous task planning
"""

import time
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import math

class PredictiveTaskPlanner:
    """Advanced predictive planning for proactive assistance"""
    
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
        self.prediction_models = {}
        self.confidence_threshold = 0.7
        self.planning_horizon_hours = 24
        
        print("🔮 Predictive Task Planner initialized")
    
    def generate_predictive_plan(self, user_id: str, current_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive predictive plan for user"""
        
        # Get user patterns and current state
        user_patterns = self._analyze_user_patterns(user_id)
        temporal_predictions = self._predict_temporal_needs(user_id)
        contextual_predictions = self._predict_contextual_needs(user_id, current_context or {})
        
        # Generate proactive tasks
        planned_tasks = self._create_proactive_tasks(user_patterns, temporal_predictions, contextual_predictions)
        
        # Prioritize and schedule tasks
        scheduled_plan = self._schedule_proactive_tasks(planned_tasks)
        
        return {
            "user_id": user_id,
            "planning_timestamp": time.time(),
            "planning_horizon": self.planning_horizon_hours,
            "user_patterns": user_patterns,
            "temporal_predictions": temporal_predictions,
            "contextual_predictions": contextual_predictions,
            "planned_tasks": scheduled_plan,
            "confidence_score": self._calculate_plan_confidence(scheduled_plan)
        }
    
    def _analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user behavioral patterns for prediction"""
        try:
            experiences = self.memory_manager.retrieve_experiences(user_id, 100)
            
            patterns = {
                "peak_activity_times": [],
                "common_stress_triggers": [],
                "help_seeking_frequency": 0.0,
                "productivity_patterns": [],
                "emotional_cycles": []
            }
            
            # Analyze temporal patterns
            activity_hours = []
            stress_episodes = []
            help_requests = 0
            total_messages = 0
            
            for exp in experiences:
                exp_data = exp.get('experience', {})
                message = str(exp_data.get('message', '')).lower()
                emotional_context = exp_data.get('emotional_context', {})
                
                total_messages += 1
                
                # Track activity times (if timestamp available)
                timestamp = exp.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        activity_hours.append(dt.hour)
                    except:
                        pass
                
                # Track stress patterns
                if 'stress' in emotional_context or any(word in message for word in ['stress', 'overwhelmed', 'pressure']):
                    stress_episodes.append({
                        'triggers': self._extract_stress_triggers(message),
                        'intensity': emotional_context.get('stress', 0.7),
                        'timestamp': timestamp
                    })
                
                # Track help-seeking
                if any(word in message for word in ['help', 'assist', 'support', 'stuck']):
                    help_requests += 1
            
            # Calculate patterns
            if activity_hours:
                # Find peak activity hours
                from collections import Counter
                hour_counts = Counter(activity_hours)
                peak_hours = [hour for hour, count in hour_counts.most_common(3)]
                patterns["peak_activity_times"] = peak_hours
            
            if stress_episodes:
                # Find common stress triggers
                all_triggers = []
                for episode in stress_episodes:
                    all_triggers.extend(episode['triggers'])
                trigger_counts = Counter(all_triggers)
                patterns["common_stress_triggers"] = [trigger for trigger, count in trigger_counts.most_common(3)]
            
            patterns["help_seeking_frequency"] = help_requests / max(1, total_messages)
            
            return patterns
            
        except Exception as e:
            print(f"⚠️ Pattern analysis failed: {e}")
            return {"error": str(e)}
    
    def _extract_stress_triggers(self, message: str) -> List[str]:
        """Extract stress triggers from message"""
        triggers = []
        trigger_keywords = {
            'work': ['work', 'job', 'boss', 'project', 'deadline', 'meeting'],
            'time': ['time', 'deadline', 'late', 'behind', 'schedule'],
            'social': ['relationship', 'conflict', 'argument', 'social'],
            'health': ['tired', 'sick', 'health', 'sleep'],
            'financial': ['money', 'budget', 'financial', 'expensive']
        }
        
        for trigger_type, keywords in trigger_keywords.items():
            if any(keyword in message for keyword in keywords):
                triggers.append(trigger_type)
        
        return triggers
    
    def _predict_temporal_needs(self, user_id: str) -> List[Dict[str, Any]]:
        """Predict needs based on time patterns"""
        predictions = []
        current_hour = datetime.now().hour
        
        try:
            experiences = self.memory_manager.retrieve_experiences(user_id, 50)
            
            # Analyze hourly patterns
            hourly_activities = defaultdict(list)
            for exp in experiences:
                timestamp = exp.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        hourly_activities[dt.hour].append(exp.get('experience', {}))
                    except:
                        continue
            
            # Predict based on current hour
            if current_hour in hourly_activities:
                similar_activities = hourly_activities[current_hour]
                
                # Check for stress patterns at this time
                stress_count = sum(1 for act in similar_activities 
                                 if 'stress' in act.get('emotional_context', {}))
                
                if stress_count > len(similar_activities) * 0.3:
                    predictions.append({
                        "type": "stress_management_support",
                        "confidence": min(0.9, stress_count / len(similar_activities)),
                        "reasoning": f"User often experiences stress around {current_hour}:00",
                        "recommended_action": "Proactively offer stress management techniques"
                    })
                
                # Check for productivity patterns
                productivity_mentions = sum(1 for act in similar_activities
                                          if any(word in str(act.get('message', '')).lower() 
                                               for word in ['task', 'organize', 'deadline']))
                
                if productivity_mentions > 2:
                    predictions.append({
                        "type": "productivity_optimization",
                        "confidence": min(0.8, productivity_mentions / len(similar_activities)),
                        "reasoning": f"User often focuses on productivity at {current_hour}:00",
                        "recommended_action": "Offer task organization assistance"
                    })
            
            return predictions
            
        except Exception as e:
            print(f"⚠️ Temporal prediction failed: {e}")
            return []
    
    def _predict_contextual_needs(self, user_id: str, current_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict needs based on current context"""
        predictions = []
        
        try:
            # If user seems stressed based on recent activity
            if current_context.get('recent_stress_indicators', 0) > 0.6:
                predictions.append({
                    "type": "immediate_stress_relief",
                    "confidence": 0.85,
                    "reasoning": "Recent interactions show stress indicators",
                    "recommended_action": "Offer breathing exercises or quick stress relief techniques"
                })
            
            # If user has been asking lots of questions
            if current_context.get('recent_question_frequency', 0) > 0.4:
                predictions.append({
                    "type": "learning_support",
                    "confidence": 0.75,
                    "reasoning": "High question frequency suggests learning mode",
                    "recommended_action": "Prepare comprehensive explanations and resources"
                })
            
            # If user mentioned deadlines recently
            if current_context.get('deadline_mentions', 0) > 0:
                predictions.append({
                    "type": "deadline_management",
                    "confidence": 0.8,
                    "reasoning": "Recent deadline mentions suggest time pressure",
                    "recommended_action": "Offer time management and prioritization assistance"
                })
            
            return predictions
            
        except Exception as e:
            print(f"⚠️ Contextual prediction failed: {e}")
            return []
    
    def _create_proactive_tasks(self, patterns: Dict, temporal_pred: List, contextual_pred: List) -> List[Dict[str, Any]]:
        """Create specific proactive tasks based on predictions"""
        tasks = []
        
        # Create tasks from temporal predictions
        for pred in temporal_pred:
            if pred['confidence'] >= self.confidence_threshold:
                task = {
                    "id": f"temporal_{int(time.time())}_{len(tasks)}",
                    "type": "proactive_assistance",
                    "category": pred['type'],
                    "description": pred['recommended_action'],
                    "confidence": pred['confidence'],
                    "reasoning": pred['reasoning'],
                    "priority": "high" if pred['confidence'] > 0.8 else "medium",
                    "timing": "immediate",
                    "estimated_duration": 5  # minutes
                }
                tasks.append(task)
        
        # Create tasks from contextual predictions
        for pred in contextual_pred:
            if pred['confidence'] >= self.confidence_threshold:
                task = {
                    "id": f"contextual_{int(time.time())}_{len(tasks)}",
                    "type": "proactive_intervention",
                    "category": pred['type'],
                    "description": pred['recommended_action'],
                    "confidence": pred['confidence'],
                    "reasoning": pred['reasoning'],
                    "priority": "urgent" if pred['confidence'] > 0.8 else "medium",
                    "timing": "immediate",
                    "estimated_duration": 3  # minutes
                }
                tasks.append(task)
        
        # Create tasks from user patterns
        if patterns.get('help_seeking_frequency', 0) > 0.3:
            tasks.append({
                "id": f"pattern_help_{int(time.time())}",
                "type": "proactive_support",
                "category": "help_anticipation",
                "description": "Prepare comprehensive assistance based on help-seeking pattern",
                "confidence": min(0.8, patterns['help_seeking_frequency']),
                "reasoning": "User frequently seeks help - anticipate needs",
                "priority": "medium",
                "timing": "scheduled",
                "estimated_duration": 10
            })
        
        return tasks
    
    def _schedule_proactive_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Schedule proactive tasks based on priority and timing"""
        # Sort by priority and confidence
        priority_order = {"urgent": 3, "high": 2, "medium": 1, "low": 0}
        
        scheduled_tasks = sorted(tasks, 
                               key=lambda x: (priority_order.get(x.get('priority', 'low'), 0), 
                                            x.get('confidence', 0)), 
                               reverse=True)
        
        # Add scheduling information
        current_time = time.time()
        for i, task in enumerate(scheduled_tasks):
            if task.get('timing') == 'immediate':
                task['scheduled_time'] = current_time + (i * 60)  # Stagger by 1 minute
            else:
                task['scheduled_time'] = current_time + (i * 300)  # Stagger by 5 minutes
            
            task['status'] = 'scheduled'
        
        return scheduled_tasks
    
    def _calculate_plan_confidence(self, scheduled_tasks: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in the predictive plan"""
        if not scheduled_tasks:
            return 0.0
        
        total_confidence = sum(task.get('confidence', 0) for task in scheduled_tasks)
        avg_confidence = total_confidence / len(scheduled_tasks)
        
        # Weight by number of high-confidence tasks
        high_conf_tasks = sum(1 for task in scheduled_tasks if task.get('confidence', 0) > 0.8)
        confidence_boost = min(0.2, (high_conf_tasks / len(scheduled_tasks)) * 0.2)
        
        return min(1.0, avg_confidence + confidence_boost)

# Test predictive planner
if __name__ == "__main__":
    print("🧪 Testing Predictive Task Planner...")
    
    from memory.memory_manager import MemoryManager
    
    memory_manager = MemoryManager()
    planner = PredictiveTaskPlanner(memory_manager)
    
    # Test predictive planning
    plan = planner.generate_predictive_plan("test_user", {
        "recent_stress_indicators": 0.7,
        "deadline_mentions": 2,
        "recent_question_frequency": 0.3
    })
    
    print(f"✅ Generated plan with {len(plan.get('planned_tasks', []))} proactive tasks")
    print(f"Plan confidence: {plan.get('confidence_score', 0):.2f}")
    
    for task in plan.get('planned_tasks', [])[:3]:  # Show first 3 tasks
        print(f"  - {task['category']}: {task['description']} (confidence: {task['confidence']:.2f})")
    
    print("🎉 Predictive Task Planner test complete!")
