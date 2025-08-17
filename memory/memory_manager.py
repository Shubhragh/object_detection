import json
import time
from typing import Dict, Any, List
from sqlalchemy import create_engine, text
from config.settings import settings
from sqlalchemy.orm import sessionmaker

class MemoryManager:
    def __init__(self):
        self.engine = create_engine(settings.POSTGRES_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def store_experience(self, user_id: str, experience: Dict[str, Any], 
                        emotional_context: Dict[str, Any] = None, 
                        importance: float = 0.5) -> bool:
        """Store a user experience in memory"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO memory_experiences 
                    (user_id, experience_data, emotional_context, importance_score)
                    VALUES (:user_id, :experience_data, :emotional_context, :importance_score)
                """), {
                    "user_id": user_id,
                    "experience_data": json.dumps(experience),
                    "emotional_context": json.dumps(emotional_context or {}),
                    "importance_score": importance
                })
                conn.commit()
                print(f"💾 Stored experience for user: {user_id}")
                return True
        except Exception as e:
            print(f"❌ Failed to store experience: {e}")
            return False
    
    def retrieve_experiences(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent experiences for a user - FIXED JSON parsing"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT experience_data, emotional_context, timestamp, importance_score
                    FROM memory_experiences 
                    WHERE user_id = :user_id
                    ORDER BY timestamp DESC
                    LIMIT :limit
                """), {"user_id": user_id, "limit": limit})
                
                experiences = []
                for row in result:
                    # Simple fix for the JSON parsing issue
                    try:
                        exp_data = json.loads(row.experience_data) if isinstance(row.experience_data, str) else row.experience_data
                        emo_data = json.loads(row.emotional_context) if isinstance(row.emotional_context, str) else row.emotional_context
                    except:
                        exp_data = {"content": str(row.experience_data)}
                        emo_data = {"mood": str(row.emotional_context)}
                    
                    experiences.append({
                        "experience": exp_data,
                        "emotional_context": emo_data,
                        "timestamp": row.timestamp.isoformat(),
                        "importance": row.importance_score
                    })
                
                print(f"📖 Retrieved {len(experiences)} experiences for {user_id}")
                return experiences
        except Exception as e:
            print(f"❌ Failed to retrieve experiences: {e}")
            return []
    
    def find_similar_experiences(self, user_id: str, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find experiences similar to query"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT experience_data, emotional_context, timestamp, importance_score
                    FROM memory_experiences 
                    WHERE user_id = :user_id 
                    AND experience_data::text ILIKE :query
                    ORDER BY importance_score DESC, timestamp DESC
                    LIMIT :limit
                """), {"user_id": user_id, "query": f"%{query_text}%", "limit": limit})
                
                similar_experiences = []
                for row in result:
                    try:
                        exp_data = json.loads(row.experience_data) if isinstance(row.experience_data, str) else row.experience_data
                        emo_data = json.loads(row.emotional_context) if isinstance(row.emotional_context, str) else row.emotional_context
                    except:
                        exp_data = {"content": str(row.experience_data)}
                        emo_data = {"mood": str(row.emotional_context)}
                    
                    similar_experiences.append({
                        "experience": exp_data,
                        "emotional_context": emo_data,
                        "timestamp": row.timestamp.isoformat(),
                        "importance": row.importance_score
                    })
                
                print(f"🔍 Found {len(similar_experiences)} similar experiences")
                return similar_experiences
        except Exception as e:
            print(f"❌ Failed to find similar experiences: {e}")
            return []
    
    def log_event(self, event_type: str, event_data: Dict[str, Any], source: str):
        """Log system events"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO event_log (event_type, event_data, source_agent)
                    VALUES (:event_type, :event_data, :source_agent)
                """), {
                    "event_type": event_type,
                    "event_data": json.dumps(event_data),
                    "source_agent": source
                })
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Failed to log event: {e}")
            return False

    # ===== ENHANCED MEMORY FEATURES (PROPERLY INDENTED INSIDE CLASS) =====
    
    def store_enhanced_experience(self, user_id: str, experience: Dict[str, Any], 
                               emotional_context: Dict[str, Any] = None, 
                               importance: float = 0.5) -> bool:
        """Enhanced experience storage with emotional intelligence"""
        try:
            # Create enhanced experience data
            enhanced_experience = experience.copy()
            
            # Add emotional intelligence
            if emotional_context:
                enhanced_experience['emotional_context'] = emotional_context
                enhanced_experience['emotional_intensity'] = self._calculate_emotional_intensity(emotional_context)
                enhanced_experience['memory_tags'] = self._generate_memory_tags(experience, emotional_context)
            
            # Calculate enhanced importance
            enhanced_importance = self._calculate_enhanced_importance(experience, emotional_context, importance)
            
            # Use existing store_experience method (keeps it working!)
            result = self.store_experience(user_id, enhanced_experience, emotional_context, enhanced_importance)
            
            if result:
                print(f"💾✨ Enhanced experience stored for {user_id}")
            
            return result
            
        except Exception as e:
            print(f"⚠️ Enhanced storage failed, using basic storage: {e}")
            # Fallback to original method if enhanced fails
            return self.store_experience(user_id, experience, emotional_context, importance)

    def _calculate_emotional_intensity(self, emotional_context: Dict[str, Any]) -> float:
        """Calculate emotional intensity from context"""
        if not emotional_context:
            return 0.0
        
        intensity_indicators = {
            'stress': 0.8, 'stressed': 0.8,
            'excited': 0.7, 'happy': 0.6,
            'angry': 0.9, 'frustrated': 0.7,
            'sad': 0.6, 'worried': 0.7,
            'seeking_help': 0.5, 'positive': 0.4,
            'negative': 0.6, 'confused': 0.4, 'calm': 0.2
        }
        
        max_intensity = 0.0
        for emotion, value in emotional_context.items():
            emotion_key = emotion.lower()
            if emotion_key in intensity_indicators:
                if isinstance(value, (int, float)):
                    max_intensity = max(max_intensity, value * intensity_indicators[emotion_key])
                else:
                    max_intensity = max(max_intensity, intensity_indicators[emotion_key])
        
        return min(max_intensity, 1.0)

    def _generate_memory_tags(self, experience: Dict[str, Any], emotional_context: Dict[str, Any] = None) -> List[str]:
        """Generate semantic tags for better memory indexing"""
        tags = []
        
        # Content-based tags
        if 'type' in experience:
            tags.append(f"type:{experience['type']}")
        
        # Extract keywords from message content
        if 'message' in experience:
            message = experience['message'].lower()
            keywords = ['work', 'stress', 'help', 'time', 'family', 'health', 'money', 'learning', 'happy', 'sad']
            for keyword in keywords:
                if keyword in message:
                    tags.append(f"topic:{keyword}")
        
        # Emotional tags
        if emotional_context:
            for emotion in emotional_context.keys():
                tags.append(f"emotion:{emotion.lower()}")
        
        # Temporal tags  
        hour = int(time.time() % 86400 // 3600)  # Hours since midnight
        if 6 <= hour < 12:
            tags.append("time:morning")
        elif 12 <= hour < 18:
            tags.append("time:afternoon")
        else:
            tags.append("time:evening")
        
        return tags

    def _calculate_enhanced_importance(self, experience: Dict[str, Any], 
                                     emotional_context: Dict[str, Any] = None, 
                                     base_importance: float = 0.5) -> float:
        """Calculate enhanced importance score"""
        importance = base_importance
        
        # Boost importance for emotional content
        if emotional_context:
            emotional_intensity = self._calculate_emotional_intensity(emotional_context)
            importance += emotional_intensity * 0.3
        
        # Boost importance for longer messages
        if 'message' in experience and len(str(experience['message'])) > 100:
            importance += 0.1
        
        # Boost importance for help requests
        if 'message' in experience:
            message = str(experience['message']).lower()
            if any(word in message for word in ['help', 'stressed', 'urgent', 'important']):
                importance += 0.2
        
        return min(importance, 1.0)

    def get_enhanced_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive memory statistics with enhancements"""
        try:
            # Get experiences using existing method
            experiences = self.retrieve_experiences(user_id, 50)
            
            if not experiences:
                return {"total_experiences": 0, "status": "no_data"}
            
            # Calculate enhanced metrics
            total_exp = len(experiences)
            importance_scores = []
            emotional_intensities = []
            
            for exp in experiences:
                exp_data = exp.get('experience', {})
                importance_scores.append(exp.get('importance', 0.5))
                emotional_intensities.append(exp_data.get('emotional_intensity', 0.0))
            
            avg_importance = sum(importance_scores) / len(importance_scores) if importance_scores else 0.5
            avg_emotional_intensity = sum(emotional_intensities) / len(emotional_intensities) if emotional_intensities else 0.0
            
            return {
                "total_experiences": total_exp,
                "average_importance": round(avg_importance, 2),
                "average_emotional_intensity": round(avg_emotional_intensity, 2),
                "recent_experiences": min(total_exp, 20),
                "memory_health": "excellent" if total_exp > 50 else "good" if total_exp > 10 else "developing",
                "enhanced_features": "active"
            }
            
        except Exception as e:
            print(f"❌ Enhanced stats failed: {e}")
            return {"total_experiences": len(self.retrieve_experiences(user_id, 10)), "status": "basic"}


# Test it
if __name__ == "__main__":
    print("🧪 Testing Enhanced Memory Manager...")
    
    memory = MemoryManager()
    
    # Test basic functionality
    basic_success = memory.store_experience("test_user", {"message": "hello"}, {"mood": "happy"})
    print(f"✅ Basic storage: {basic_success}")
    
    # Test enhanced functionality
    enhanced_success = memory.store_enhanced_experience(
        "test_user",
        {"type": "chat", "message": "I'm feeling stressed about work again"},
        {"stress": 0.8, "anxiety": 0.6},
        0.7
    )
    print(f"✅ Enhanced storage: {enhanced_success}")
    
    # Test retrieval
    experiences = memory.retrieve_experiences("test_user")
    print(f"✅ Retrieved: {len(experiences)} experiences")
    
    # Test enhanced stats
    stats = memory.get_enhanced_memory_stats("test_user")
    print(f"✅ Enhanced stats: {stats}")
    
    print("🎉 Enhanced memory manager test complete!")
