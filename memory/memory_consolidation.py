"""
FIXED Memory Consolidation with AI-powered theme identification
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class MemoryConsolidationEngine:
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
        
        # Initialize AI agents for intelligent consolidation
        try:
            from agents.emotional_analysis_agent import EmotionalAnalysisAgent
            from agents.intent_classification_agent import IntentClassificationAgent
            
            self.emotional_agent = EmotionalAnalysisAgent()
            self.intent_agent = IntentClassificationAgent()
            
            # Initialize agents
            self.emotional_agent.initialize()
            self.intent_agent.initialize()
            
            self.ai_enhanced = True
            print("🧠✨ Memory Consolidation Engine initialized with AI")
        except Exception as e:
            print(f"⚠️ AI agents not available for consolidation: {e}")
            self.ai_enhanced = False
        
        self.min_experiences_for_pattern = 3
        self.consolidation_strength_threshold = 0.6
        self.pattern_reinforcement_factor = 0.15

    def _identify_memory_themes_with_ai(self, experiences: List[Dict]) -> Dict[str, List]:
        """COMPLETELY REWRITTEN: AI-powered theme identification"""
        themes = defaultdict(list)
        
        if not self.ai_enhanced:
            return self._fallback_theme_identification(experiences)
        
        print(f"🤖 Using AI to analyze {len(experiences)} experiences for themes...")
        
        # Analyze each experience with AI
        for exp in experiences:
            exp_data = exp.get('experience', {})
            message = str(exp_data.get('message', ''))
            
            if not message or len(message.strip()) < 5:
                continue
                
            try:
                # AI emotional analysis
                emotional_analysis = self.emotional_agent.analyze_emotional_context(message)
                emotions = emotional_analysis.get('emotions', {})
                
                # AI intent classification
                intent_analysis = self.intent_agent.classify_intent(message, emotional_analysis)
                intent = intent_analysis.get('intent', 'general')
                suggested_agent = intent_analysis.get('suggested_agent', 'general')
                
                # AI-POWERED THEME CLASSIFICATION
                
                # Stress-related themes
                if emotions.get('stress', 0) > 0.5 or emotions.get('anxiety', 0) > 0.5:
                    if intent in ['request_help', 'emotional_support']:
                        themes['stress_management_needs'].append(exp)
                    else:
                        themes['stress_response_patterns'].append(exp)
                
                # Work-related themes
                if 'ProductivityAgent' in suggested_agent:
                    if emotions.get('stress', 0) > 0.4:
                        themes['work_stress_management'].append(exp)
                    else:
                        themes['productivity_focused_interactions'].append(exp)
                
                # Help-seeking themes
                if intent == 'request_help' or emotions.get('seeking_help', 0) > 0.4:
                    if emotions.get('confusion', 0) > 0.5:
                        themes['learning_support_needs'].append(exp)
                    else:
                        themes['general_help_seeking'].append(exp)
                
                # Communication themes
                if 'CommunicationAgent' in suggested_agent:
                    themes['communication_optimization'].append(exp)
                
                # Emotional wellness themes
                if intent == 'emotional_support':
                    themes['emotional_wellness_focus'].append(exp)
                
                # Learning and curiosity themes
                if emotions.get('curiosity', 0) > 0.4 or intent == 'question':
                    themes['learning_curiosity_pattern'].append(exp)
                
                # High engagement themes
                if intent_analysis.get('importance', 0) > 0.7:
                    themes['high_engagement_interactions'].append(exp)
                    
            except Exception as e:
                print(f"⚠️ AI analysis failed for experience, using fallback: {e}")
                # Add to general theme as fallback
                themes['general_interactions'].append(exp)
        
        # Filter themes with minimum experiences
        filtered_themes = {
            theme: experiences_list 
            for theme, experiences_list in themes.items() 
            if len(experiences_list) >= self.min_experiences_for_pattern
        }
        
        print(f"🎯 AI identified {len(filtered_themes)} themes: {list(filtered_themes.keys())}")
        return dict(filtered_themes)

    def _fallback_theme_identification(self, experiences: List[Dict]) -> Dict[str, List]:
        """Fallback theme identification when AI is not available"""
        themes = defaultdict(list)
        
        for exp in experiences:
            exp_data = exp.get('experience', {})
            message = str(exp_data.get('message', '')).lower()
            emotional_context = exp_data.get('emotional_context', {})
            
            # Basic keyword-based classification (fallback only)
            if any(word in message for word in ['help', 'assist', 'support', 'stuck']):
                themes['help_seeking_pattern'].append(exp)
            
            if 'stress' in emotional_context or any(word in message for word in ['stress', 'overwhelmed']):
                themes['stress_related_interactions'].append(exp)
                
            if any(word in message for word in ['work', 'job', 'project', 'deadline']):
                themes['work_related_discussions'].append(exp)
        
        return dict(themes)

    def _consolidate_theme_with_ai(self, theme: str, experiences: List[Dict]) -> Dict[str, Any]:
        """AI-ENHANCED theme consolidation"""
        consolidation = {
            "theme": theme,
            "total_experiences": len(experiences),
            "pattern_strength": min(1.0, len(experiences) / 10.0),
            "ai_insights": [],
            "emotional_profile": {},
            "behavioral_insights": [],
            "frequency_analysis": {},
            "consolidated_knowledge": ""
        }
        
        if not self.ai_enhanced:
            return self._basic_theme_consolidation(theme, experiences)
        
        # AI-powered consolidation
        try:
            # Aggregate AI analyses
            all_emotions = defaultdict(list)
            all_intents = []
            message_sample = []
            
            for exp in experiences[:10]:  # Analyze up to 10 experiences
                exp_data = exp.get('experience', {})
                message = str(exp_data.get('message', ''))
                
                if message:
                    message_sample.append(message[:100])  # First 100 chars
                    
                    # Get AI analysis if available in stored data
                    if 'ai_emotional_analysis' in exp_data:
                        emotions = exp_data['ai_emotional_analysis'].get('emotions', {})
                        for emotion, score in emotions.items():
                            all_emotions[emotion].append(score)
                    
                    if 'ai_intent_analysis' in exp_data:
                        intent = exp_data['ai_intent_analysis'].get('intent', '')
                        if intent:
                            all_intents.append(intent)
            
            # Generate emotional profile
            for emotion, scores in all_emotions.items():
                consolidation["emotional_profile"][emotion] = sum(scores) / len(scores)
            
            # Generate AI insights based on theme and patterns
            consolidation["ai_insights"] = self._generate_ai_insights(theme, consolidation["emotional_profile"], all_intents)
            
            # Generate behavioral insights
            consolidation["behavioral_insights"] = self._generate_behavioral_insights(theme, experiences)
            
            # Generate consolidated knowledge summary
            consolidation["consolidated_knowledge"] = self._generate_knowledge_summary(theme, consolidation)
            
        except Exception as e:
            print(f"⚠️ AI consolidation failed for {theme}: {e}")
            return self._basic_theme_consolidation(theme, experiences)
        
        return consolidation

    def _generate_ai_insights(self, theme: str, emotional_profile: Dict, intents: List[str]) -> List[str]:
        """Generate insights using AI analysis"""
        insights = []
        
        # Emotional insights
        dominant_emotions = sorted(emotional_profile.items(), key=lambda x: x[1], reverse=True)[:3]
        if dominant_emotions:
            top_emotion, score = dominant_emotions
            insights.append(f"Dominant emotional pattern: {top_emotion} (intensity: {score:.2f})")
        
        # Intent insights
        if intents:
            intent_counts = Counter(intents)
            most_common_intent = intent_counts.most_common(1)[0]
            insights.append(f"Primary user intent: {most_common_intent} ({most_common_intent[1]} occurrences)")
        
        # Theme-specific insights
        if 'stress' in theme:
            if emotional_profile.get('stress', 0) > 0.6:
                insights.append("High stress intensity detected - proactive intervention recommended")
            insights.append("User shows consistent stress patterns requiring ongoing support")
        
        elif 'help' in theme or 'support' in theme:
            insights.append("User demonstrates proactive help-seeking behavior")
            if emotional_profile.get('curiosity', 0) > 0.5:
                insights.append("Help-seeking combined with learning curiosity")
        
        elif 'learning' in theme or 'curiosity' in theme:
            insights.append("Strong learning orientation with consistent question patterns")
        
        return insights[:5]

    def _generate_behavioral_insights(self, theme: str, experiences: List[Dict]) -> List[str]:
        """Generate behavioral insights from experience patterns"""
        insights = []
        
        # Frequency analysis
        freq_per_week = len(experiences) / 4  # Assuming 4-week analysis window
        
        if freq_per_week > 3:
            insights.append(f"High frequency pattern: {freq_per_week:.1f} occurrences per week")
        elif freq_per_week > 1:
            insights.append(f"Regular pattern: {freq_per_week:.1f} occurrences per week")
        else:
            insights.append(f"Occasional pattern: {freq_per_week:.1f} occurrences per week")
        
        # Pattern consistency
        if len(experiences) > 7:
            insights.append("Highly consistent behavioral pattern")
        elif len(experiences) > 4:
            insights.append("Moderately consistent pattern")
        
        # Theme-specific behavioral insights
        if 'stress' in theme.lower():
            insights.append("User experiences recurring stress episodes")
            insights.append("Benefits from proactive stress management support")
        
        elif 'help' in theme.lower():
            insights.append("User actively seeks assistance when needed")
            insights.append("Responds well to guided problem-solving")
        
        elif 'work' in theme.lower() or 'productivity' in theme.lower():
            insights.append("Work-focused interaction pattern")
            insights.append("Values productivity optimization")
        
        return insights

    def _generate_knowledge_summary(self, theme: str, consolidation: Dict) -> str:
        """Generate comprehensive knowledge summary"""
        total_exp = consolidation["total_experiences"]
        pattern_strength = consolidation["pattern_strength"]
        
        summary = f"Theme '{theme}' shows {pattern_strength:.1%} pattern strength across {total_exp} interactions. "
        
        # Add emotional context
        emotions = consolidation.get("emotional_profile", {})
        if emotions:
            top_emotion = max(emotions, key=emotions.get)
            summary += f"Primary emotional association: {top_emotion} ({emotions[top_emotion]:.2f}). "
        
        # Add frequency context
        freq = total_exp / 4  # Per week
        if freq > 2:
            summary += f"High frequency pattern ({freq:.1f}/week) indicating strong user behavior tendency."
        else:
            summary += f"Moderate frequency pattern ({freq:.1f}/week) showing emerging behavior."
        
        return summary

    def consolidate_memories(self, user_id: str) -> Dict[str, Any]:
        """ENHANCED main consolidation method with AI"""
        print(f"🔄🤖 AI-powered memory consolidation for {user_id}...")
        
        try:
            experiences = self.memory_manager.retrieve_experiences(user_id, 100)
            
            if len(experiences) < self.min_experiences_for_pattern:
                return {
                    "status": "insufficient_data",
                    "experiences_count": len(experiences),
                    "message": "Need more interactions for AI consolidation"
                }

            # AI-powered theme identification
            themes = self._identify_memory_themes_with_ai(experiences)
            
            # AI-enhanced consolidation
            consolidated_knowledge = {}
            for theme, theme_experiences in themes.items():
                consolidated_knowledge[theme] = self._consolidate_theme_with_ai(theme, theme_experiences)
            
            # Generate AI insights
            insights = self._generate_consolidation_insights_ai(consolidated_knowledge)
            
            # Store consolidated memories
            self._store_consolidated_memories(user_id, consolidated_knowledge)
            
            result = {
                "status": "success",
                "ai_powered": True,
                "themes_identified": len(themes),
                "themes_consolidated": len(consolidated_knowledge),
                "consolidated_themes": list(consolidated_knowledge.keys()),
                "insights": insights,
                "experiences_processed": len(experiences),
                "ai_confidence": self._calculate_ai_consolidation_confidence(consolidated_knowledge)
            }
            
            print(f"✅🤖 AI consolidation complete: {len(consolidated_knowledge)} themes, confidence: {result['ai_confidence']:.2f}")
            return result
            
        except Exception as e:
            print(f"❌ AI consolidation failed: {e}")
            return {"status": "error", "error": str(e)}

    def _generate_consolidation_insights_ai(self, consolidated_knowledge: Dict[str, Any]) -> List[str]:
        """Generate insights from AI-consolidated knowledge"""
        insights = []
        
        themes = list(consolidated_knowledge.keys())
        
        # AI-powered cross-theme insights
        if 'stress_management_needs' in themes and 'work_related' in str(themes):
            work_stress = consolidated_knowledge.get('stress_management_needs', {})
            insights.append(f"Work-related stress is a major pattern ({work_stress.get('total_experiences', 0)} instances) requiring proactive intervention")
        
        if 'help_seeking_pattern' in str(themes):
            help_data = consolidated_knowledge.get('general_help_seeking', consolidated_knowledge.get('learning_support_needs', {}))
            if help_data:
                insights.append(f"User actively seeks assistance ({help_data.get('total_experiences', 0)} requests) - proactive guidance highly effective")
        
        if 'learning_curiosity_pattern' in themes:
            learning_data = consolidated_knowledge[themes[0] if 'learning' in themes else 'learning_curiosity_pattern']
            insights.append(f"Strong learning orientation detected ({learning_data.get('total_experiences', 0)} instances) - detailed explanations preferred")
        
        # Pattern strength insights
        high_strength_themes = [
            theme for theme, data in consolidated_knowledge.items()
            if data.get('pattern_strength', 0) > 0.7
        ]
        
        if len(high_strength_themes) >= 2:
            insights.append(f"Multiple strong behavioral patterns identified: {', '.join(high_strength_themes[:3])}")
        
        # Emotional insights
        for theme, data in consolidated_knowledge.items():
            emotions = data.get('emotional_profile', {})
            if emotions.get('stress', 0) > 0.6:
                insights.append(f"High stress intensity in {theme} - monitor for intervention opportunities")
        
        return insights[:7]

    def _calculate_ai_consolidation_confidence(self, consolidated_knowledge: Dict) -> float:
        """Calculate confidence in AI consolidation"""
        if not consolidated_knowledge:
            return 0.0
        
        total_experiences = sum(data.get('total_experiences', 0) for data in consolidated_knowledge.values())
        avg_pattern_strength = sum(data.get('pattern_strength', 0) for data in consolidated_knowledge.values()) / len(consolidated_knowledge)
        
        # AI enhancement bonus
        ai_bonus = 0.2 if self.ai_enhanced else 0.0
        
        base_confidence = min(1.0, (total_experiences / 50.0 * 0.6) + (avg_pattern_strength * 0.4) + ai_bonus)
        
        return round(base_confidence, 2)

    # Keep existing methods for compatibility
    def get_consolidated_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights from previously consolidated memories"""
        try:
            experiences = self.memory_manager.retrieve_experiences(user_id, 200)
            consolidated_memories = [
                exp for exp in experiences
                if exp.get('experience', {}).get('type') == 'consolidated_memory'
            ]

            if not consolidated_memories:
                return {"status": "no_consolidations", "message": "No consolidated memories found"}

            insights = {
                "total_consolidations": len(consolidated_memories),
                "active_patterns": [],
                "behavioral_profile": {},
                "recommendations": []
            }

            for memory in consolidated_memories:
                exp_data = memory.get('experience', {})
                theme = exp_data.get('theme', 'unknown')
                consolidation_data = exp_data.get('consolidation_data', {})
                
                insights["active_patterns"].append({
                    "theme": theme,
                    "strength": consolidation_data.get('pattern_strength', 0.0),
                    "experiences": consolidation_data.get('total_experiences', 0),
                    "insights": consolidation_data.get('ai_insights', consolidation_data.get('behavioral_insights', []))[:2]
                })

            # Sort by pattern strength
            insights["active_patterns"].sort(key=lambda x: x['strength'], reverse=True)
            
            return insights

        except Exception as e:
            print(f"❌ Failed to get consolidated insights: {e}")
            return {"status": "error", "error": str(e)}

    def _store_consolidated_memories(self, user_id: str, consolidated_knowledge: Dict[str, Any]):
        """Store consolidated memories with AI enhancements"""
        try:
            for theme, consolidation in consolidated_knowledge.items():
                if hasattr(self.memory_manager, 'store_enhanced_experience'):
                    self.memory_manager.store_enhanced_experience(
                        user_id,
                        {
                            "type": "consolidated_memory",
                            "theme": theme,
                            "consolidation_data": consolidation,
                            "knowledge_summary": consolidation["consolidated_knowledge"],
                            "ai_enhanced": self.ai_enhanced
                        },
                        emotional_context={
                            "consolidation": 1.0, 
                            "pattern_strength": consolidation["pattern_strength"],
                            **consolidation.get("emotional_profile", {})
                        },
                        importance=0.9
                    )
                else:
                    self.memory_manager.store_experience(
                        user_id,
                        {
                            "type": "consolidated_memory",
                            "theme": theme,
                            "summary": consolidation["consolidated_knowledge"],
                            "ai_enhanced": self.ai_enhanced
                        },
                        {"consolidation": 1.0},
                        0.9
                    )

            print(f"💾🤖 Stored {len(consolidated_knowledge)} AI-enhanced consolidated memories")

        except Exception as e:
            print(f"⚠️ Failed to store consolidated memories: {e}")
