"""
Pattern Recognition Engine for AI Life Operating System
Analyzes behavioral, emotional, and temporal patterns from memory data
"""


import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import Counter, defaultdict
from memory.memory_manager import MemoryManager



class PatternRecognitionEngine:
    def __init__(self, memory_manager: MemoryManager = None):
        self.memory_manager = memory_manager or MemoryManager()
        
        # Pattern detection thresholds
        self.min_pattern_occurrences = 3
        self.confidence_threshold = 0.6
        self.analysis_window_days = 14
        
        print("🔍 Pattern Recognition Engine initialized")
    
    def analyze_all_patterns(self, user_id: str, days: int = 14) -> Dict[str, Any]:
        """Main method: Analyze all user patterns comprehensively"""
        print(f"🔍 Running comprehensive pattern analysis for {user_id}...")
        
        # Get experiences from memory manager
        try:
            experiences = self.memory_manager.retrieve_experiences(user_id, 200)
        except Exception as e:
            print(f"⚠️ Error retrieving experiences: {e}")
            experiences = []
        
        if not experiences:
            return self._empty_analysis_result("Insufficient interaction data")
        
        # Run all pattern analyses
        analysis_result = {
            "user_id": user_id,
            "analysis_timestamp": time.time(),
            "total_experiences": len(experiences),
            "analysis_period_days": days,
            
            # Pattern categories
            "behavioral_patterns": self._detect_behavioral_patterns(experiences),
            "emotional_patterns": self._detect_emotional_patterns(experiences), 
            "temporal_patterns": self._detect_temporal_patterns(experiences),
            "communication_patterns": self._detect_communication_patterns(experiences),
            "help_seeking_patterns": self._detect_help_seeking_patterns(experiences),
            
            # Overall insights
            "pattern_summary": {},
            "confidence_score": 0.0,
            "actionable_insights": []
        }
        
        # Generate summary and insights
        analysis_result["pattern_summary"] = self._generate_pattern_summary(analysis_result)
        analysis_result["confidence_score"] = self._calculate_overall_confidence(analysis_result)
        analysis_result["actionable_insights"] = self._generate_insights(analysis_result)
        
        print(f"✅ Pattern analysis complete: {analysis_result['confidence_score']} confidence")
        return analysis_result
    
    def _detect_behavioral_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Detect behavioral patterns in user interactions"""
        patterns = {
            "detected_behaviors": [],
            "behavior_frequency": {},
            "consistency_score": 0.0
        }
        
        # Analyze message patterns
        user_messages = [exp for exp in experiences 
                        if exp.get('experience', {}).get('type') == 'user_message']
        
        if len(user_messages) >= self.min_pattern_occurrences:
            # Message length patterns
            lengths = [len(exp.get('experience', {}).get('message', '')) for exp in user_messages]
            if lengths:
                avg_length = sum(lengths) / len(lengths)
                
                if avg_length < 30:
                    patterns["detected_behaviors"].append("concise_communicator")
                elif avg_length > 100:
                    patterns["detected_behaviors"].append("detailed_communicator")
            
            # Topic consistency
            topics = []
            for exp in user_messages:
                message = exp.get('experience', {}).get('message', '').lower()
                topics.extend(self._extract_topics(message))
            
            if topics:
                topic_counts = Counter(topics)
                dominant_topics = [topic for topic, count in topic_counts.items() if count >= 3]
                if dominant_topics:
                    patterns["detected_behaviors"].append(f"focus_on_{dominant_topics[0]}")
                    # Fix: Convert list to string for dictionary key
                    patterns["behavior_frequency"][str(dominant_topics)] = dict(topic_counts)
        
        patterns["consistency_score"] = min(len(patterns["detected_behaviors"]) * 0.2, 1.0)
        return patterns
    
    def _detect_emotional_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Detect emotional patterns and trends"""
        patterns = {
            "emotional_trends": [],
            "stress_frequency": 0.0,
            "emotional_stability": 0.0,
            "dominant_emotions": {}
        }
        
        # Extract emotional data
        emotional_experiences = []
        for exp in experiences:
            exp_data = exp.get('experience', {})
            if 'emotional_context' in exp_data or 'emotional_intensity' in exp_data:
                emotional_experiences.append(exp_data)
        
        if len(emotional_experiences) >= self.min_pattern_occurrences:
            # Stress pattern analysis
            stress_count = 0
            total_intensity = 0
            emotion_counts = defaultdict(int)
            
            for exp_data in emotional_experiences:
                emotional_context = exp_data.get('emotional_context', {})
                intensity = exp_data.get('emotional_intensity', 0.0)
                total_intensity += intensity
                
                # Count stress occurrences
                if isinstance(emotional_context, dict) and 'stress' in emotional_context:
                    stress_count += 1
                elif isinstance(emotional_context, str) and 'stress' in emotional_context.lower():
                    stress_count += 1
                
                # Count all emotions
                if isinstance(emotional_context, dict):
                    for emotion in emotional_context.keys():
                        emotion_counts[emotion] += 1
                elif isinstance(emotional_context, str):
                    # Simple emotion detection from string
                    for emotion in ['stress', 'happy', 'sad', 'angry', 'excited', 'calm']:
                        if emotion in emotional_context.lower():
                            emotion_counts[emotion] += 1
            
            # Calculate patterns
            patterns["stress_frequency"] = stress_count / len(emotional_experiences)
            patterns["emotional_stability"] = max(0.0, 1.0 - (total_intensity / len(emotional_experiences)))
            patterns["dominant_emotions"] = dict(Counter(emotion_counts).most_common(3))
            
            # Detect emotional trends
            if patterns["stress_frequency"] > 0.3:
                patterns["emotional_trends"].append("high_stress_frequency")
            if patterns["emotional_stability"] > 0.7:
                patterns["emotional_trends"].append("emotionally_stable")
            elif patterns["emotional_stability"] < 0.3:
                patterns["emotional_trends"].append("emotionally_variable")
        
        return patterns
    
    def _detect_temporal_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Detect temporal patterns in user activity"""
        patterns = {
            "activity_periods": [],
            "peak_hours": [],
            "schedule_consistency": 0.0
        }
        
        # Extract timestamps
        timestamps = []
        for exp in experiences:
            timestamp_str = exp.get('timestamp', '')
            if timestamp_str:
                try:
                    # Parse various timestamp formats
                    if isinstance(timestamp_str, str):
                        if 'T' in timestamp_str:
                            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        else:
                            dt = datetime.fromtimestamp(float(timestamp_str))
                    else:
                        dt = datetime.fromtimestamp(float(timestamp_str))
                    timestamps.append(dt.hour)
                except (ValueError, TypeError) as e:
                    continue
        
        if len(timestamps) >= self.min_pattern_occurrences:
            # Analyze hourly activity
            hour_counts = Counter(timestamps)
            
            # Find peak activity periods
            if hour_counts:
                max_activity = max(hour_counts.values())
                peak_hours = [hour for hour, count in hour_counts.items() 
                             if count >= max_activity * 0.7]
                
                patterns["peak_hours"] = sorted(peak_hours)
                
                # Determine activity periods
                if any(6 <= hour < 12 for hour in peak_hours):
                    patterns["activity_periods"].append("morning_active")
                if any(12 <= hour < 18 for hour in peak_hours):
                    patterns["activity_periods"].append("afternoon_active")  
                if any(18 <= hour <= 23 or 0 <= hour < 6 for hour in peak_hours):
                    patterns["activity_periods"].append("evening_active")
                
                # Calculate schedule consistency - Fixed hashable type error
                active_hours_count = len([h for h in range(24) if hour_counts.get(h, 0) > 0])
                patterns["schedule_consistency"] = max(0.0, 1.0 - (active_hours_count / 24.0))
        
        return patterns
    
    def _detect_communication_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Detect communication style patterns"""
        patterns = {
            "communication_style": [],
            "response_preferences": [],
            "interaction_frequency": 0.0
        }
        
        user_messages = [exp for exp in experiences 
                        if exp.get('experience', {}).get('type') == 'user_message']
        
        if user_messages:
            # Analyze communication style
            question_count = 0
            exclamation_count = 0
            
            for exp in user_messages:
                message = exp.get('experience', {}).get('message', '')
                if '?' in message:
                    question_count += 1
                if '!' in message:
                    exclamation_count += 1
            
            total_messages = len(user_messages)
            
            if total_messages > 0:
                if question_count / total_messages > 0.4:
                    patterns["communication_style"].append("inquisitive")
                if exclamation_count / total_messages > 0.3:
                    patterns["communication_style"].append("expressive")
                
                # Calculate interaction frequency (messages per day estimate)
                time_span = max(7, self.analysis_window_days)  # Use analysis window or minimum 7 days
                patterns["interaction_frequency"] = len(user_messages) / time_span
        
        return patterns
    
    def _detect_help_seeking_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Detect help-seeking behavior patterns"""
        patterns = {
            "help_frequency": 0.0,
            "help_topics": [],
            "problem_solving_style": []
        }
        
        help_requests = []
        user_messages = []
        
        for exp in experiences:
            exp_data = exp.get('experience', {})
            if exp_data.get('type') == 'user_message':
                message = exp_data.get('message', '').lower()
                user_messages.append(message)
                
                help_indicators = ['help', 'assist', 'support', 'stuck', 'confused', 'how to', 'need']
                if any(indicator in message for indicator in help_indicators):
                    help_requests.append(message)
        
        if user_messages:
            patterns["help_frequency"] = len(help_requests) / len(user_messages)
            
            # Analyze help topics
            all_topics = []
            for request in help_requests:
                all_topics.extend(self._extract_topics(request))
            
            if all_topics:
                topic_counter = Counter(all_topics)
                patterns["help_topics"] = [topic for topic, count in topic_counter.most_common(3)]
            
            # Determine problem-solving style
            if patterns["help_frequency"] > 0.3:
                patterns["problem_solving_style"].append("frequent_help_seeker")
            elif patterns["help_frequency"] < 0.1:
                patterns["problem_solving_style"].append("independent_problem_solver")
            else:
                patterns["problem_solving_style"].append("balanced_help_seeker")
        
        return patterns
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message text"""
        topics = []
        message_lower = message.lower()
        
        topic_keywords = {
            'work': ['work', 'job', 'career', 'office', 'project', 'deadline', 'meeting'],
            'stress': ['stress', 'overwhelmed', 'pressure', 'anxiety', 'worried'],
            'time': ['time', 'schedule', 'busy', 'calendar', 'manage', 'planning'],
            'health': ['health', 'tired', 'sleep', 'exercise', 'wellness', 'fitness'],
            'learning': ['learn', 'understand', 'study', 'confused', 'education'],
            'technology': ['computer', 'software', 'app', 'technical', 'digital'],
            'relationship': ['family', 'friend', 'colleague', 'relationship', 'social'],
            'productivity': ['productive', 'efficient', 'organize', 'focus', 'task'],
            'emotional': ['feel', 'emotion', 'mood', 'upset', 'happy', 'sad']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _generate_pattern_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of all detected patterns"""
        all_patterns = []
        
        # Collect all detected patterns
        for category, data in analysis.items():
            if isinstance(data, dict):
                if 'detected_behaviors' in data:
                    all_patterns.extend(data.get('detected_behaviors', []))
                if 'emotional_trends' in data:
                    all_patterns.extend(data.get('emotional_trends', []))
                if 'activity_periods' in data:
                    all_patterns.extend(data.get('activity_periods', []))
                if 'communication_style' in data:
                    all_patterns.extend(data.get('communication_style', []))
                if 'problem_solving_style' in data:
                    all_patterns.extend(data.get('problem_solving_style', []))
        
        return {
            "total_patterns_detected": len(all_patterns),
            "pattern_categories": len([k for k in analysis.keys() if k.endswith('_patterns')]),
            "strongest_patterns": all_patterns[:5] if all_patterns else [],
            "pattern_diversity": len(set(all_patterns)) if all_patterns else 0
        }
    
    def _calculate_overall_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence in pattern analysis"""
        total_experiences = analysis.get('total_experiences', 0)
        total_patterns = analysis.get('pattern_summary', {}).get('total_patterns_detected', 0)
        
        # Base confidence on data quantity and pattern diversity
        data_confidence = min(total_experiences / 50.0, 1.0)  # Max at 50 experiences
        pattern_confidence = min(total_patterns / 10.0, 1.0)  # Max at 10 patterns
        
        # Ensure minimum confidence with some data
        if total_experiences > 0:
            base_confidence = max(0.1, (data_confidence + pattern_confidence) / 2.0)
        else:
            base_confidence = 0.0
        
        return round(base_confidence, 2)
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from patterns"""
        insights = []
        
        # Behavioral insights
        behavioral = analysis.get('behavioral_patterns', {})
        detected_behaviors = behavioral.get('detected_behaviors', [])
        
        if 'concise_communicator' in detected_behaviors:
            insights.append("Provide brief, direct responses - user prefers concise communication")
        elif 'detailed_communicator' in detected_behaviors:
            insights.append("User appreciates detailed explanations - provide comprehensive responses")
        
        # Emotional insights
        emotional = analysis.get('emotional_patterns', {})
        if emotional.get('stress_frequency', 0) > 0.3:
            insights.append("Monitor for stress indicators and offer proactive support")
        if 'emotionally_stable' in emotional.get('emotional_trends', []):
            insights.append("User maintains good emotional balance - focus on maintaining current strategies")
        elif 'high_stress_frequency' in emotional.get('emotional_trends', []):
            insights.append("Consider stress management interventions and regular check-ins")
        
        # Temporal insights
        temporal = analysis.get('temporal_patterns', {})
        activity_periods = temporal.get('activity_periods', [])
        
        if 'morning_active' in activity_periods:
            insights.append("Schedule important interactions for morning hours when user is most active")
        elif 'evening_active' in activity_periods:
            insights.append("User is most active in evenings - optimize support for after-hours")
        
        if temporal.get('schedule_consistency', 0) > 0.7:
            insights.append("User maintains consistent schedule - can predict availability patterns")
        
        # Communication insights
        communication = analysis.get('communication_patterns', {})
        comm_style = communication.get('communication_style', [])
        
        if 'inquisitive' in comm_style:
            insights.append("User asks many questions - prepare comprehensive explanations")
        if 'expressive' in comm_style:
            insights.append("User communicates expressively - match energy level in responses")
        
        # Help-seeking insights
        help_seeking = analysis.get('help_seeking_patterns', {})
        if help_seeking.get('help_frequency', 0) > 0.3:
            insights.append("User benefits from proactive assistance - anticipate needs before explicit requests")
        elif help_seeking.get('help_frequency', 0) < 0.1:
            insights.append("User prefers independence - offer suggestions rather than detailed guidance")
        
        # Topic-based insights
        help_topics = help_seeking.get('help_topics', [])
        if help_topics:
            insights.append(f"User frequently needs help with {help_topics[0]} - prepare specialized resources")
        
        return insights[:7]  # Return top 7 insights
    
    def _empty_analysis_result(self, reason: str) -> Dict[str, Any]:
        """Return empty analysis result with reason"""
        return {
            "user_id": "",
            "analysis_timestamp": time.time(),
            "total_experiences": 0,
            "analysis_period_days": 0,
            "behavioral_patterns": {"detected_behaviors": [], "behavior_frequency": {}, "consistency_score": 0.0},
            "emotional_patterns": {"emotional_trends": [], "stress_frequency": 0.0, "emotional_stability": 0.0, "dominant_emotions": {}},
            "temporal_patterns": {"activity_periods": [], "peak_hours": [], "schedule_consistency": 0.0},
            "communication_patterns": {"communication_style": [], "response_preferences": [], "interaction_frequency": 0.0},
            "help_seeking_patterns": {"help_frequency": 0.0, "help_topics": [], "problem_solving_style": []},
            "pattern_summary": {"total_patterns_detected": 0, "pattern_categories": 0, "strongest_patterns": [], "pattern_diversity": 0},
            "confidence_score": 0.0,
            "actionable_insights": ["Continue interacting to build pattern recognition data"],
            "message": reason
        }
    
    def debug_predict_user_needs(self, user_id: str) -> Dict[str, Any]:
        """Debug version to identify why predictions aren't generating"""
        print(f"🔍 DEBUG: Analyzing predictions for {user_id}...")
        
        try:
            # Get recent patterns
            analysis = self.analyze_all_patterns(user_id, 7)
            print(f"DEBUG: Analysis confidence: {analysis.get('confidence_score', 0)}")
            
            patterns = analysis.get('patterns', {})
            print(f"DEBUG: Available pattern categories: {list(patterns.keys())}")
            
            predictions = []
            confidence_scores = []
            
            # Check emotional patterns
            emotional = patterns.get('emotional_patterns', {})
            print(f"DEBUG: Emotional patterns: {emotional}")
            
            if emotional.get('stress_episodes', 0) > 0:
                confidence = min(0.8, emotional.get('stress_frequency', 0) + 0.3)
                predictions.append({
                    "predicted_need": "stress_management_support",
                    "confidence": confidence,
                    "reasoning": f"Detected {emotional['stress_episodes']} stress episodes"
                })
                confidence_scores.append(confidence)
                print(f"DEBUG: Added stress prediction (confidence: {confidence})")
            
            # Check help-seeking patterns  
            help_seeking = patterns.get('help_seeking_patterns', {})
            print(f"DEBUG: Help-seeking patterns: {help_seeking}")
            
            if help_seeking.get('help_request_frequency', 0) > 2:
                confidence = min(0.75, help_seeking.get('help_request_frequency', 0) / 10)
                predictions.append({
                    "predicted_need": "proactive_assistance",
                    "confidence": confidence,
                    "reasoning": f"High help request frequency: {help_seeking['help_request_frequency']}"
                })
                confidence_scores.append(confidence)
                print(f"DEBUG: Added help prediction (confidence: {confidence})")
            
            # Check communication patterns
            comm = patterns.get('communication_patterns', {})
            print(f"DEBUG: Communication patterns: {comm}")
            
            if comm.get('interaction_frequency', 0) > 0.3:
                predictions.append({
                    "predicted_need": "engagement_optimization", 
                    "confidence": 0.6,
                    "reasoning": "High interaction frequency suggests engagement focus"
                })
                confidence_scores.append(0.6)
                print(f"DEBUG: Added engagement prediction")
            
            overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            result = {
                "predictions": predictions,
                "prediction_confidence": round(overall_confidence, 2),
                "based_on_patterns": len(patterns)
            }
            
            print(f"DEBUG: Final result: {len(predictions)} predictions, confidence: {overall_confidence:.2f}")
            return result
            
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            return {"predictions": [], "prediction_confidence": 0.0}
    
    def predict_user_needs(self, user_id: str) -> Dict[str, Any]:
        """FIXED: Extract predictions from consolidated memory insights"""
        print(f"🔮 Predicting user needs for {user_id}...")
        
        try:
            predictions = []
            
            # Get consolidated insights directly
            try:
                consolidation = self.memory_manager.consolidation_engine.consolidate_memories(user_id)
                insights = consolidation.get('insights', [])
                
                print(f"DEBUG: Found {len(insights)} consolidated insights")
                
                # Parse insights for predictions with FIXED parsing logic
                for insight in insights:
                    insight_lower = insight.lower()
                    
                    if 'stress' in insight_lower and 'pattern' in insight_lower:
                        # FIXED: Safe number extraction
                        import re
                        numbers = re.findall(r'\d+', insight)
                        
                        # FIXED: Proper type checking and conversion
                        if numbers and isinstance(numbers, list) and len(numbers) > 0:
                            try:
                                stress_count = int(numbers[0])  # Convert first number string to int
                            except (ValueError, TypeError):
                                stress_count = 1  # Fallback value
                        else:
                            stress_count = 1
                        
                        predictions.append({
                            "predicted_need": "stress_management_support",
                            "confidence": min(0.9, 0.6 + (stress_count * 0.05)),
                            "reasoning": insight,
                            "suggested_actions": ["Proactive stress management", "Monitor stress triggers"]
                        })
                        print(f"✅ Added stress prediction from: {insight}")
                    
                    elif 'assistance' in insight_lower or 'help' in insight_lower:
                        # FIXED: Safe number extraction for help requests
                        import re
                        numbers = re.findall(r'\d+', insight)
                        
                        if numbers and isinstance(numbers, list) and len(numbers) > 0:
                            try:
                                help_count = int(numbers[0])
                            except (ValueError, TypeError):
                                help_count = 1
                        else:
                            help_count = 1
                        
                        predictions.append({
                            "predicted_need": "proactive_assistance",
                            "confidence": min(0.85, 0.5 + (help_count * 0.01)),
                            "reasoning": insight,
                            "suggested_actions": ["Anticipate user needs", "Offer proactive guidance"]
                        })
                        print(f"✅ Added assistance prediction from: {insight}")
                    
                    elif 'learning' in insight_lower:
                        predictions.append({
                            "predicted_need": "learning_optimization",
                            "confidence": 0.7,
                            "reasoning": insight,
                            "suggested_actions": ["Optimize learning approach", "Provide study techniques"]
                        })
                        print(f"✅ Added learning prediction from: {insight}")
            
            except Exception as e:
                print(f"⚠️ Consolidation-based predictions failed: {e}")
                # Fallback to direct analysis if consolidation fails
                print("🔄 Using fallback direct analysis...")
            
            # Fallback: Direct pattern analysis if no predictions yet
            if not predictions:
                print("🔄 Using fallback pattern analysis...")
                
                # Get recent experiences and analyze directly
                experiences = self.memory_manager.retrieve_experiences(user_id, 50)
                
                stress_count = 0
                help_count = 0
                work_count = 0
                
                for exp in experiences:
                    exp_data = exp.get('experience', {})
                    message = str(exp_data.get('message', '')).lower()
                    emotional_context = exp_data.get('emotional_context', {})
                    
                    if 'stress' in emotional_context or any(word in message for word in ['stress', 'overwhelmed', 'pressure']):
                        stress_count += 1
                    
                    if any(word in message for word in ['help', 'assist', 'support', 'guidance']):
                        help_count += 1
                    
                    if any(word in message for word in ['work', 'job', 'project', 'deadline']):
                        work_count += 1
                
                # Generate predictions from direct analysis with LOWER thresholds
                if stress_count >= 2:  # Lowered threshold
                    predictions.append({
                        "predicted_need": "stress_management_support",
                        "confidence": min(0.9, 0.5 + (stress_count * 0.1)),
                        "reasoning": f"Detected {stress_count} stress-related interactions",
                        "suggested_actions": ["Stress management techniques", "Wellness check-ins"]
                    })
                
                if help_count >= 3:  # Lowered threshold
                    predictions.append({
                        "predicted_need": "proactive_assistance", 
                        "confidence": min(0.85, 0.4 + (help_count * 0.05)),
                        "reasoning": f"User requests help frequently ({help_count} instances)",
                        "suggested_actions": ["Proactive guidance", "Anticipate needs"]
                    })
                
                if work_count >= 5:  # Lowered threshold
                    predictions.append({
                        "predicted_need": "productivity_optimization",
                        "confidence": 0.75,
                        "reasoning": f"Strong work focus detected ({work_count} mentions)",
                        "suggested_actions": ["Productivity tips", "Workflow optimization"]
                    })
            
            # Calculate overall confidence
            overall_confidence = 0.0
            if predictions:
                confidences = [p['confidence'] for p in predictions]
                overall_confidence = sum(confidences) / len(confidences)
            
            result = {
                "predictions": predictions,
                "prediction_confidence": round(overall_confidence, 2),
                "based_on_experiences": len(self.memory_manager.retrieve_experiences(user_id, 10))
            }
            
            print(f"✅ Generated {len(predictions)} predictions with {overall_confidence:.2f} confidence")
            return result
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            import traceback
            traceback.print_exc()
            return {"predictions": [], "prediction_confidence": 0.0}


    def get_pattern_insights_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a quick summary of user patterns for dashboard display"""
        analysis = self.analyze_all_patterns(user_id, 14)
        
        return {
            "user_id": user_id,
            "overall_confidence": analysis.get('confidence_score', 0.0),
            "total_patterns": analysis.get('pattern_summary', {}).get('total_patterns_detected', 0),
            "key_behaviors": analysis.get('behavioral_patterns', {}).get('detected_behaviors', [])[:3],
            "stress_level": "high" if analysis.get('emotional_patterns', {}).get('stress_frequency', 0) > 0.3 else "normal",
            "peak_activity": analysis.get('temporal_patterns', {}).get('activity_periods', []),
            "top_insights": analysis.get('actionable_insights', [])[:3]
        }



# Test the pattern recognition engine
if __name__ == "__main__":
    print("🧪 Testing Pattern Recognition Engine...")
    
    # Initialize engine
    try:
        pattern_engine = PatternRecognitionEngine()
        
        # Test with sample user
        print("🔍 Testing pattern analysis...")
        analysis = pattern_engine.analyze_all_patterns("test_user")
        print(f"✅ Pattern analysis: {analysis.get('confidence_score', 0)} confidence")
        print(f"📊 Total patterns detected: {analysis.get('pattern_summary', {}).get('total_patterns_detected', 0)}")
        
        # Test predictions
        print("🔮 Testing need predictions...")
        predictions = pattern_engine.predict_user_needs("test_user")
        print(f"✅ Predictions: {len(predictions.get('predictions', []))} needs predicted")
        print(f"🎯 Prediction confidence: {predictions.get('prediction_confidence', 0)}")
        
        # Test summary
        print("📋 Testing insights summary...")
        summary = pattern_engine.get_pattern_insights_summary("test_user")
        print(f"✅ Summary generated with {summary.get('total_patterns', 0)} patterns")
        
        print("🎉 Pattern Recognition Engine test complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
