"""
Memory Consolidation System for AI Life Operating System
Organizes, synthesizes, and evolves memories over time
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class MemoryConsolidationEngine:
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
        
        # Consolidation parameters
        self.min_experiences_for_pattern = 3
        self.consolidation_strength_threshold = 0.6
        self.pattern_reinforcement_factor = 0.15
        
        print("🧠 Memory Consolidation Engine initialized")
    
    def consolidate_memories(self, user_id: str) -> Dict[str, Any]:
        """Run memory consolidation process"""
        print(f"🔄 Consolidating memories for {user_id}...")
        
        try:
            # Get all user experiences
            experiences = self.memory_manager.retrieve_experiences(user_id, 100)
            
            if len(experiences) < self.min_experiences_for_pattern:
                return {
                    "status": "insufficient_data",
                    "experiences_count": len(experiences),
                    "message": "Need more interactions for consolidation"
                }
            
            # Identify memory themes and patterns
            themes = self._identify_memory_themes(experiences)
            
            # Create consolidated knowledge
            consolidated_knowledge = {}
            for theme, theme_experiences in themes.items():
                if len(theme_experiences) >= self.min_experiences_for_pattern:
                    consolidated_knowledge[theme] = self._consolidate_theme(theme, theme_experiences)
            
            # Generate insights from consolidated memories
            insights = self._generate_consolidation_insights(consolidated_knowledge)
            
            # Store consolidated memories (in enhanced format)
            self._store_consolidated_memories(user_id, consolidated_knowledge)
            
            result = {
                "status": "success",
                "themes_identified": len(themes),
                "themes_consolidated": len(consolidated_knowledge),
                "consolidated_themes": list(consolidated_knowledge.keys()),
                "insights": insights,
                "experiences_processed": len(experiences)
            }
            
            print(f"✅ Memory consolidation complete: {len(consolidated_knowledge)} themes consolidated")
            return result
            
        except Exception as e:
            print(f"❌ Memory consolidation failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def _identify_memory_themes(self, experiences: List[Dict]) -> Dict[str, List]:
        """Identify recurring themes across experiences"""
        themes = defaultdict(list)
        
        for exp in experiences:
            exp_data = exp.get('experience', {})
            message = str(exp_data.get('message', '')).lower()
            emotional_context = exp_data.get('emotional_context', {})
            exp_type = exp_data.get('type', '')
            
            # Work-related patterns
            if any(word in message for word in ['work', 'job', 'boss', 'project', 'deadline', 'office']):
                if any(emotion in emotional_context for emotion in ['stress', 'overwhelmed']):
                    themes['work_stress_management'].append(exp)
                else:
                    themes['work_general_topics'].append(exp)
            
            # Help-seeking patterns
            if any(word in message for word in ['help', 'assist', 'support', 'stuck', 'confused']):
                themes['help_seeking_behavior'].append(exp)
            
            # Learning and curiosity patterns
            if any(word in message for word in ['learn', 'understand', 'explain', 'how', 'what', 'why']):
                themes['learning_curiosity'].append(exp)
            
            # System interaction patterns
            if exp_type == 'user_message' and any(word in message for word in ['what', 'who', 'system', 'agent']):
                themes['system_exploration'].append(exp)
            
            # Emotional patterns
            if 'stress' in emotional_context:
                themes['stress_response_pattern'].append(exp)
            if any(emotion in emotional_context for emotion in ['positive', 'happy', 'excited']):
                themes['positive_interaction_pattern'].append(exp)
            
            # Communication style patterns
            if len(message) > 100:
                themes['detailed_communication_style'].append(exp)
            elif len(message) < 30 and '?' in message:
                themes['concise_question_style'].append(exp)
        
        return dict(themes)
    
    def _consolidate_theme(self, theme: str, experiences: List[Dict]) -> Dict[str, Any]:
        """Consolidate experiences into organized knowledge"""
        consolidation = {
            "theme": theme,
            "total_experiences": len(experiences),
            "pattern_strength": min(1.0, len(experiences) / 10.0),  # Max at 10 experiences
            "key_patterns": [],
            "emotional_profile": {},
            "behavioral_insights": [],
            "frequency_analysis": {},
            "evolution_timeline": [],
            "consolidated_knowledge": ""
        }
        
        # Analyze emotional patterns within theme
        all_emotions = []
        for exp in experiences:
            exp_data = exp.get('experience', {})
            emotions = exp_data.get('emotional_context', {})
            all_emotions.extend(emotions.keys())
        
        if all_emotions:
            emotion_counts = Counter(all_emotions)
            consolidation["emotional_profile"] = dict(emotion_counts.most_common(5))
        
        # Generate behavioral insights based on theme
        if theme == 'work_stress_management':
            consolidation["behavioral_insights"] = [
                "User experiences work-related stress regularly",
                "Stress often triggered by deadlines and management issues",
                "Seeks assistance when overwhelmed",
                "Benefits from proactive stress management support"
            ]
            consolidation["consolidated_knowledge"] = f"User shows consistent work stress pattern across {len(experiences)} interactions, primarily related to deadlines and management conflicts."
        
        elif theme == 'help_seeking_behavior':
            consolidation["behavioral_insights"] = [
                "User actively seeks assistance when needed",
                "Prefers guided problem-solving approach",
                "Appreciates detailed explanations",
                "Shows learning-oriented mindset"
            ]
            consolidation["consolidated_knowledge"] = f"User demonstrates proactive help-seeking behavior with {len(experiences)} assistance requests, indicating openness to learning and support."
        
        elif theme == 'learning_curiosity':
            consolidation["behavioral_insights"] = [
                "User exhibits strong curiosity and learning drive",
                "Asks thoughtful, exploratory questions", 
                "Values understanding over quick answers",
                "Engages deeply with explanations"
            ]
            consolidation["consolidated_knowledge"] = f"User shows consistent learning curiosity with {len(experiences)} exploratory interactions, preferring comprehensive understanding."
        
        elif theme == 'system_exploration':
            consolidation["behavioral_insights"] = [
                "User actively explores system capabilities",
                "Shows interest in understanding AI architecture",
                "Tests system boundaries and functions",
                "Values transparency in AI operations"
            ]
            consolidation["consolidated_knowledge"] = f"User demonstrates systematic exploration of AI capabilities across {len(experiences)} interactions, seeking understanding of system architecture."
        
        # Frequency analysis
        consolidation["frequency_analysis"] = {
            "occurrences_per_week": len(experiences) / 4,  # Assuming 4-week period
            "trend": "increasing" if len(experiences) > 7 else "stable",
            "consistency_score": min(1.0, len(experiences) / 15.0)
        }
        
        # Key patterns (simplified)
        consolidation["key_patterns"] = [
            f"Recurring {theme} behavior",
            f"Consistent emotional associations",
            f"Frequency: {consolidation['frequency_analysis']['occurrences_per_week']:.1f} per week"
        ]
        
        return consolidation
    
    def _generate_consolidation_insights(self, consolidated_knowledge: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from consolidated memories"""
        insights = []
        
        # Analyze consolidated themes for insights
        themes = list(consolidated_knowledge.keys())
        
        if 'work_stress_management' in themes:
            work_data = consolidated_knowledge['work_stress_management']
            insights.append(f"Work stress is a recurring pattern ({work_data['total_experiences']} instances) - consider proactive wellness support")
        
        if 'help_seeking_behavior' in themes:
            help_data = consolidated_knowledge['help_seeking_behavior']
            insights.append(f"User actively seeks assistance ({help_data['total_experiences']} requests) - proactive guidance recommended")
        
        if 'learning_curiosity' in themes:
            learning_data = consolidated_knowledge['learning_curiosity']
            insights.append(f"Strong learning orientation detected ({learning_data['total_experiences']} instances) - provide detailed explanations")
        
        if 'system_exploration' in themes:
            system_data = consolidated_knowledge['system_exploration']
            insights.append(f"User explores system capabilities thoroughly ({system_data['total_experiences']} interactions) - transparency valued")
        
        # Cross-theme insights
        if len(themes) >= 3:
            insights.append("Rich behavioral profile developed - enable advanced personalization features")
        
        if any('stress' in theme for theme in themes):
            insights.append("Stress management patterns identified - monitor for proactive intervention opportunities")
        
        return insights[:5]  # Return top 5 insights
    
    def _store_consolidated_memories(self, user_id: str, consolidated_knowledge: Dict[str, Any]):
        """Store consolidated memories back to memory system"""
        try:
            for theme, consolidation in consolidated_knowledge.items():
                # Store as enhanced experience
                if hasattr(self.memory_manager, 'store_enhanced_experience'):
                    self.memory_manager.store_enhanced_experience(
                        user_id,
                        {
                            "type": "consolidated_memory",
                            "theme": theme,
                            "consolidation_data": consolidation,
                            "knowledge_summary": consolidation["consolidated_knowledge"]
                        },
                        emotional_context={"consolidation": 1.0, "pattern_strength": consolidation["pattern_strength"]},
                        importance=0.9  # High importance for consolidated memories
                    )
                else:
                    # Fallback to basic storage
                    self.memory_manager.store_experience(
                        user_id,
                        {
                            "type": "consolidated_memory", 
                            "theme": theme,
                            "summary": consolidation["consolidated_knowledge"]
                        },
                        {"consolidation": 1.0},
                        0.9
                    )
            
            print(f"💾 Stored {len(consolidated_knowledge)} consolidated memories")
            
        except Exception as e:
            print(f"⚠️ Failed to store consolidated memories: {e}")
    
    def get_consolidated_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights from previously consolidated memories"""
        try:
            # Get consolidated memories from storage
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
                    "insights": consolidation_data.get('behavioral_insights', [])[:2]
                })
            
            # Sort by pattern strength
            insights["active_patterns"].sort(key=lambda x: x['strength'], reverse=True)
            
            return insights
            
        except Exception as e:
            print(f"❌ Failed to get consolidated insights: {e}")
            return {"status": "error", "error": str(e)}

# Test memory consolidation
if __name__ == "__main__":
    print("🧪 Testing Memory Consolidation Engine...")
    
    from memory.memory_manager import MemoryManager
    
    memory_manager = MemoryManager()
    consolidation_engine = MemoryConsolidationEngine(memory_manager)
    
    # Run consolidation test
    result = consolidation_engine.consolidate_memories("test_user")
    print(f"✅ Consolidation result: {result}")
    
    # Get insights
    insights = consolidation_engine.get_consolidated_insights("test_user")
    print(f"✅ Consolidated insights: {insights}")
    
    print("🎉 Memory Consolidation Engine test complete!")
