"""
CORRECTED Pattern Recognition Engine - Fixed missing analyze_all_patterns method
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
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
        """FIXED: Main method for comprehensive pattern analysis"""
        print(f"🔍 Running comprehensive pattern analysis for {user_id}...")
        
        try:
            # Get experiences from memory manager
            experiences = self.memory_manager.retrieve_experiences(user_id, 200)
            
            if not experiences:
                return self._empty_analysis_result("Insufficient interaction data")

            # Filter experiences by time window if needed
            cutoff_time = datetime.now() - timedelta(days=days)
            recent_experiences = []
            
            for exp in experiences:
                try:
                    timestamp_str = exp.get('timestamp', '')
                    if timestamp_str:
                        exp_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if exp_time >= cutoff_time:
                            recent_experiences.append(exp)
                except:
                    # Include experiences with invalid timestamps
                    recent_experiences.append(exp)
            
            if not recent_experiences:
                recent_experiences = experiences[:50]  # Use recent 50 if time filtering fails

            # Run all pattern analyses
            analysis_result = {
                "user_id": user_id,
                "analysis_timestamp": time.time(),
                "total_experiences": len(recent_experiences),
                "analysis_period_days": days,
                
                # Pattern categories
                "behavioral_patterns": self._detect_behavioral_patterns(recent_experiences),
                "emotional_patterns": self._detect_emotional_patterns(recent_experiences),
                "temporal_patterns": self._detect_temporal_patterns(recent_experiences),
                "communication_patterns": self._detect_communication_patterns(recent_experiences),
                "help_seeking_patterns": self._detect_help_seeking_patterns(recent_experiences),
                
                # Overall insights
                "pattern_summary": {},
                "confidence_score": 0.0,
                "actionable_insights": []
            }

            # Generate summary and insights
            analysis_result["pattern_summary"] = self._generate_pattern_summary(analysis_result)
            analysis_result["confidence_score"] = self._calculate_overall_confidence(analysis_result)
            analysis_result["actionable_insights"] = self._generate_insights(analysis_result)

            print(f"✅ Pattern analysis complete: {analysis_result['confidence_score']:.2f} confidence")
            return analysis_result

        except Exception as e:
            print(f"❌ Pattern analysis failed: {e}")
            return self._empty_analysis_result(f"Analysis error: {str(e)}")

    def _detect_behavioral_patterns(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Detect behavioral patterns in user interactions"""
        patterns = {
            "detected_behaviors": [],
            "behavior_frequency": {},
            "consistency_score": 0.0
        }

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
                    patterns["behavior_frequency"] = dict(topic_counts.most_common(5))

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
        stress_count = 0
        total_intensity = 0.0
        emotion_counts = defaultdict(int)

        for exp in experiences:
            exp_data = exp.get('experience', {})
            message = exp_data.get('message', '').lower()
            emotional_context = exp_data.get('emotional_context', {})
            
            # Check for stress indicators in message
            if any(word in message for word in ['stress', 'overwhelmed', 'anxiety', 'worried', 'pressure']):
                stress_count += 1
                emotion_counts['stress'] += 1

            # Check for positive emotions
            if any(word in message for word in ['happy', 'excited', 'great', 'good', 'amazing']):
                emotion_counts['positive'] += 1

            # Check for negative emotions
            if any(word in message for word in ['sad', 'upset', 'frustrated', 'angry', 'disappointed']):
                emotion_counts['negative'] += 1

            # Process stored emotional context
            if emotional_context:
                emotional_experiences.append(exp_data)
                if isinstance(emotional_context, dict):
                    for emotion, value in emotional_context.items():
                        emotion_counts[emotion] += 1
                        if isinstance(value, (int, float)):
                            total_intensity += value
                        else:
                            total_intensity += 0.5

        total_messages = len(experiences)
        if total_messages > 0:
            patterns["stress_frequency"] = stress_count / total_messages
            patterns["emotional_stability"] = max(0.0, 1.0 - (total_intensity / max(1, len(emotional_experiences))))
            patterns["dominant_emotions"] = dict(Counter(emotion_counts).most_common(5))

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
                    if 'T' in timestamp_str:
                        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.fromtimestamp(float(timestamp_str))
                    timestamps.append(dt.hour)
                except (ValueError, TypeError):
                    continue

        if len(timestamps) >= self.min_pattern_occurrences:
            # Analyze hourly activity
            hour_counts = Counter(timestamps)
            
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

                # Calculate schedule consistency
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
                time_span = max(7, self.analysis_window_days)
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
        data_confidence = min(total_experiences / 50.0, 1.0)
        pattern_confidence = min(total_patterns / 10.0, 1.0)

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

        return insights[:7]

    def predict_user_needs(self, user_id: str) -> Dict[str, Any]:
        """CORRECTED: Predict user needs based on comprehensive pattern analysis"""
        print(f"🔮 Predicting user needs for {user_id}...")

        try:
            # Get comprehensive pattern analysis
            analysis = self.analyze_all_patterns(user_id, 7)
            
            predictions = []
            
            # Extract pattern data correctly
            emotional_patterns = analysis.get('emotional_patterns', {})
            behavioral_patterns = analysis.get('behavioral_patterns', {})
            help_seeking_patterns = analysis.get('help_seeking_patterns', {})
            communication_patterns = analysis.get('communication_patterns', {})

            print(f"DEBUG: Emotional stress frequency: {emotional_patterns.get('stress_frequency', 0)}")
            print(f"DEBUG: Help seeking frequency: {help_seeking_patterns.get('help_frequency', 0)}")

            # Stress management prediction
            stress_freq = emotional_patterns.get('stress_frequency', 0.0)
            if stress_freq > 0.2:  # Lowered threshold
                predictions.append({
                    "predicted_need": "stress_management_support",
                    "confidence": min(0.9, 0.6 + (stress_freq * 0.4)),
                    "reasoning": f"Stress detected in {stress_freq:.1%} of recent interactions",
                    "suggested_actions": ["Proactive stress monitoring", "Stress relief techniques"]
                })
                print(f"✅ Added stress prediction (confidence: {min(0.9, 0.6 + (stress_freq * 0.4)):.2f})")

            # Help-seeking prediction
            help_freq = help_seeking_patterns.get('help_frequency', 0.0)
            if help_freq > 0.15:  # Lowered threshold
                predictions.append({
                    "predicted_need": "proactive_assistance",
                    "confidence": min(0.85, 0.5 + (help_freq * 0.5)),
                    "reasoning": f"User requests help frequently ({help_freq:.1%} of messages)",
                    "suggested_actions": ["Anticipate needs", "Proactive guidance"]
                })
                print(f"✅ Added help prediction (confidence: {min(0.85, 0.5 + (help_freq * 0.5)):.2f})")

            # Communication pattern prediction
            comm_freq = communication_patterns.get('interaction_frequency', 0.0)
            if comm_freq > 1.0:  # More than 1 message per day
                predictions.append({
                    "predicted_need": "engagement_optimization",
                    "confidence": 0.7,
                    "reasoning": f"High interaction frequency ({comm_freq:.1f} messages/day)",
                    "suggested_actions": ["Regular engagement", "Response optimization"]
                })
                print(f"✅ Added engagement prediction (confidence: 0.7)")

            # Calculate overall confidence
            overall_confidence = 0.0
            if predictions:
                confidences = [p['confidence'] for p in predictions]
                overall_confidence = sum(confidences) / len(confidences)

            result = {
                "predictions": predictions,
                "prediction_confidence": round(overall_confidence, 2),
                "based_on_experiences": len(self.memory_manager.retrieve_experiences(user_id, 10)),
                "analysis_used": {
                    "emotional_patterns": bool(emotional_patterns),
                    "behavioral_patterns": bool(behavioral_patterns),
                    "help_seeking_patterns": bool(help_seeking_patterns),
                    "communication_patterns": bool(communication_patterns)
                }
            }

            print(f"✅ Generated {len(predictions)} predictions with {overall_confidence:.2f} confidence")
            return result

        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            import traceback
            traceback.print_exc()
            return {"predictions": [], "prediction_confidence": 0.0, "error": str(e)}

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

# Test the corrected pattern recognition engine
if __name__ == "__main__":
    print("🧪 Testing Corrected Pattern Recognition Engine...")
    
    from memory.memory_manager import MemoryManager
    memory_manager = MemoryManager()
    
    pattern_engine = PatternRecognitionEngine(memory_manager)
    
    # Test analysis
    analysis = pattern_engine.analyze_all_patterns("test_user")
    print(f"✅ Analysis result: {analysis.get('confidence_score', 0)} confidence")
    
    # Test predictions
    predictions = pattern_engine.predict_user_needs("test_user")
    print(f"✅ Predictions: {len(predictions.get('predictions', []))} needs predicted")
    
    print("🎉 Pattern Recognition Engine test complete!")
