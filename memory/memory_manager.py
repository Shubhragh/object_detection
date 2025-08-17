"""
CORRECTED Memory Manager - Fixed integration, enhanced features, and reliable storage
"""

import json
import time
from typing import Dict, Any, List
from sqlalchemy import create_engine, text
from config.settings import settings
from sqlalchemy.orm import sessionmaker

class MemoryManager:
    def __init__(self):
        """Initialize memory manager with proper database connection"""
        try:
            self.engine = create_engine(
                settings.POSTGRES_URL,
                pool_size=5,
                max_overflow=10,
                pool_recycle=3600
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print("💾 Memory Manager initialized with database connection")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def store_experience(self, user_id: str, experience: Dict[str, Any],
                        emotional_context: Dict[str, Any] = None,
                        importance: float = 0.5) -> bool:
        """Store a user experience in memory with proper error handling"""
        try:
            # Validate inputs
            if not user_id or not experience:
                print("⚠️ Invalid input: user_id and experience required")
                return False
            
            importance = max(0.0, min(1.0, importance))  # Clamp between 0-1
            
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO memory_experiences
                    (user_id, experience_data, emotional_context, importance_score)
                    VALUES (:user_id, :experience_data, :emotional_context, :importance_score)
                """), {
                    "user_id": user_id,
                    "experience_data": json.dumps(experience, default=str),
                    "emotional_context": json.dumps(emotional_context or {}, default=str),
                    "importance_score": importance
                })
                conn.commit()
                
            print(f"💾 Stored experience for user: {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to store experience: {e}")
            return False

    def store_enhanced_experience(self, user_id: str, experience: Dict[str, Any],
                                emotional_context: Dict[str, Any] = None,
                                importance: float = 0.5) -> bool:
        """CORRECTED: Enhanced experience storage with proper integration"""
        try:
            # Create enhanced experience data
            enhanced_experience = experience.copy()
            
            # Add emotional intensity if emotional context provided
            if emotional_context:
                enhanced_experience['emotional_intensity'] = self._calculate_emotional_intensity(emotional_context)
                enhanced_experience['memory_tags'] = self._generate_memory_tags(experience, emotional_context)
            else:
                enhanced_experience['emotional_intensity'] = 0.0
                enhanced_experience['memory_tags'] = self._generate_memory_tags(experience, {})
            
            # Calculate enhanced importance
            enhanced_importance = self._calculate_enhanced_importance(experience, emotional_context, importance)
            
            # Store using standard method
            result = self.store_experience(user_id, enhanced_experience, emotional_context, enhanced_importance)
            
            if result:
                print(f"💾✨ Enhanced experience stored for {user_id}")
                
            return result
            
        except Exception as e:
            print(f"⚠️ Enhanced storage failed, using basic storage: {e}")
            # Fallback to basic storage
            return self.store_experience(user_id, experience, emotional_context, importance)

    def _calculate_emotional_intensity(self, emotional_context: Dict[str, Any]) -> float:
        """ADDED: Calculate emotional intensity from context"""
        if not emotional_context:
            return 0.0

        intensity_indicators = {
            'stress': 0.8, 'stressed': 0.8, 'anxiety': 0.7,
            'excited': 0.7, 'happy': 0.6, 'joy': 0.6,
            'angry': 0.9, 'frustrated': 0.7, 'upset': 0.6,
            'sad': 0.6, 'worried': 0.7, 'concerned': 0.5,
            'seeking_help': 0.5, 'positive': 0.4, 'calm': 0.2,
            'negative': 0.6, 'confused': 0.4, 'uncertain': 0.3,
            'urgency': 0.8, 'emergency': 0.9
        }

        max_intensity = 0.0
        for emotion, value in emotional_context.items():
            emotion_key = emotion.lower()
            
            if emotion_key in intensity_indicators:
                if isinstance(value, (int, float)):
                    # Value is a score
                    max_intensity = max(max_intensity, value * intensity_indicators[emotion_key])
                else:
                    # Value is presence indicator
                    max_intensity = max(max_intensity, intensity_indicators[emotion_key])

        return min(max_intensity, 1.0)

    def _generate_memory_tags(self, experience: Dict[str, Any], emotional_context: Dict[str, Any] = None) -> List[str]:
        """ADDED: Generate semantic tags for better memory indexing"""
        tags = []
        
        # Experience type tags
        if 'type' in experience:
            tags.append(f"type:{experience['type']}")
        
        # Message content tags (basic keyword extraction)
        if 'message' in experience:
            message = str(experience['message']).lower()
            
            # Topic keywords
            topic_keywords = {
                'work': ['work', 'job', 'career', 'office', 'project', 'deadline', 'meeting'],
                'stress': ['stress', 'overwhelmed', 'pressure', 'anxiety', 'worried'],
                'help': ['help', 'assist', 'support', 'guidance', 'stuck'],
                'time': ['time', 'schedule', 'busy', 'calendar', 'manage'],
                'learning': ['learn', 'understand', 'study', 'confused', 'education'],
                'health': ['health', 'tired', 'sleep', 'exercise', 'wellness'],
                'social': ['family', 'friend', 'colleague', 'relationship', 'social']
            }
            
            for topic, keywords in topic_keywords.items():
                if any(keyword in message for keyword in keywords):
                    tags.append(f"topic:{topic}")
        
        # Emotional tags
        if emotional_context:
            for emotion in emotional_context.keys():
                tags.append(f"emotion:{emotion.lower()}")
        
        # Temporal tags
        hour = int(time.time() % 86400 // 3600)
        if 6 <= hour < 12:
            tags.append("time:morning")
        elif 12 <= hour < 18:
            tags.append("time:afternoon")  
        else:
            tags.append("time:evening")
        
        return list(set(tags))  # Remove duplicates

    def _calculate_enhanced_importance(self, experience: Dict[str, Any],
                                     emotional_context: Dict[str, Any] = None,
                                     base_importance: float = 0.5) -> float:
        """ADDED: Calculate enhanced importance score"""
        importance = base_importance
        
        # Boost importance for emotional content
        if emotional_context:
            emotional_intensity = self._calculate_emotional_intensity(emotional_context)
            importance += emotional_intensity * 0.3
        
        # Boost importance for longer messages
        if 'message' in experience:
            message_length = len(str(experience['message']))
            if message_length > 100:
                importance += 0.1
            elif message_length > 200:
                importance += 0.15
        
        # Boost importance for help requests and urgent content
        if 'message' in experience:
            message = str(experience['message']).lower()
            if any(word in message for word in ['help', 'urgent', 'important', 'emergency']):
                importance += 0.2
            if any(word in message for word in ['stressed', 'overwhelmed', 'anxious']):
                importance += 0.15
        
        return min(importance, 1.0)

    def retrieve_experiences(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """CORRECTED: Retrieve experiences with robust JSON parsing"""
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
                    try:
                        # Robust JSON parsing
                        if isinstance(row.experience_data, str):
                            exp_data = json.loads(row.experience_data)
                        elif isinstance(row.experience_data, dict):
                            exp_data = row.experience_data
                        else:
                            exp_data = {"content": str(row.experience_data)}
                        
                        if isinstance(row.emotional_context, str):
                            emo_data = json.loads(row.emotional_context)
                        elif isinstance(row.emotional_context, dict):
                            emo_data = row.emotional_context
                        else:
                            emo_data = {}

                        experiences.append({
                            "experience": exp_data,
                            "emotional_context": emo_data,
                            "timestamp": row.timestamp.isoformat() if hasattr(row.timestamp, 'isoformat') else str(row.timestamp),
                            "importance": float(row.importance_score) if row.importance_score is not None else 0.5
                        })

                    except Exception as parse_error:
                        print(f"⚠️ Failed to parse experience row: {parse_error}")
                        # Create fallback experience
                        experiences.append({
                            "experience": {"content": "parsing_error", "raw_data": str(row.experience_data)},
                            "emotional_context": {},
                            "timestamp": str(row.timestamp) if row.timestamp else str(time.time()),
                            "importance": 0.5
                        })

                print(f"📖 Retrieved {len(experiences)} experiences for {user_id}")
                return experiences

        except Exception as e:
            print(f"❌ Failed to retrieve experiences: {e}")
            return []

    def find_similar_experiences(self, user_id: str, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """CORRECTED: Find similar experiences with better search"""
        try:
            with self.engine.connect() as conn:
                # Search in both experience data and emotional context
                result = conn.execute(text("""
                    SELECT experience_data, emotional_context, timestamp, importance_score
                    FROM memory_experiences
                    WHERE user_id = :user_id
                    AND (
                        experience_data::text ILIKE :query
                        OR emotional_context::text ILIKE :query
                    )
                    ORDER BY importance_score DESC, timestamp DESC
                    LIMIT :limit
                """), {"user_id": user_id, "query": f"%{query_text}%", "limit": limit})

                similar_experiences = []
                for row in result:
                    try:
                        # Use same parsing logic as retrieve_experiences
                        if isinstance(row.experience_data, str):
                            exp_data = json.loads(row.experience_data)
                        elif isinstance(row.experience_data, dict):
                            exp_data = row.experience_data
                        else:
                            exp_data = {"content": str(row.experience_data)}

                        if isinstance(row.emotional_context, str):
                            emo_data = json.loads(row.emotional_context)
                        elif isinstance(row.emotional_context, dict):
                            emo_data = row.emotional_context
                        else:
                            emo_data = {}

                        similar_experiences.append({
                            "experience": exp_data,
                            "emotional_context": emo_data,
                            "timestamp": row.timestamp.isoformat() if hasattr(row.timestamp, 'isoformat') else str(row.timestamp),
                            "importance": float(row.importance_score) if row.importance_score is not None else 0.5
                        })

                    except Exception as parse_error:
                        print(f"⚠️ Failed to parse similar experience: {parse_error}")
                        continue

                print(f"🔍 Found {len(similar_experiences)} similar experiences")
                return similar_experiences

        except Exception as e:
            print(f"❌ Failed to find similar experiences: {e}")
            return []

    def get_memory_statistics(self, user_id: str) -> Dict[str, Any]:
        """ADDED: Get comprehensive memory statistics"""
        try:
            with self.engine.connect() as conn:
                # Get basic counts
                count_result = conn.execute(text("""
                    SELECT COUNT(*) as total_count,
                           AVG(importance_score) as avg_importance,
                           MAX(timestamp) as latest_timestamp,
                           MIN(timestamp) as earliest_timestamp
                    FROM memory_experiences
                    WHERE user_id = :user_id
                """), {"user_id": user_id})
                
                row = count_result.fetchone()
                
                if row and row.total_count > 0:
                    return {
                        "total_experiences": int(row.total_count),
                        "average_importance": round(float(row.avg_importance), 2),
                        "latest_timestamp": str(row.latest_timestamp) if row.latest_timestamp else None,
                        "earliest_timestamp": str(row.earliest_timestamp) if row.earliest_timestamp else None,
                        "memory_health": "excellent" if row.total_count > 50 else "good" if row.total_count > 10 else "developing"
                    }
                else:
                    return {
                        "total_experiences": 0,
                        "memory_health": "no_data"
                    }

        except Exception as e:
            print(f"❌ Failed to get memory statistics: {e}")
            return {"total_experiences": 0, "error": str(e)}

    def log_event(self, event_type: str, event_data: Dict[str, Any], source: str) -> bool:
        """Log system events"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO event_log (event_type, event_data, source_agent)
                    VALUES (:event_type, :event_data, :source_agent)
                """), {
                    "event_type": event_type,
                    "event_data": json.dumps(event_data, default=str),
                    "source_agent": source
                })
                conn.commit()
                return True
                
        except Exception as e:
            print(f"❌ Failed to log event: {e}")
            return False

    def cleanup_old_experiences(self, user_id: str, keep_count: int = 1000) -> int:
        """ADDED: Clean up old experiences to manage database size"""
        try:
            with self.engine.connect() as conn:
                # Delete oldest experiences beyond keep_count, but preserve high-importance ones
                result = conn.execute(text("""
                    DELETE FROM memory_experiences
                    WHERE user_id = :user_id
                    AND id NOT IN (
                        SELECT id FROM memory_experiences
                        WHERE user_id = :user_id
                        ORDER BY importance_score DESC, timestamp DESC
                        LIMIT :keep_count
                    )
                """), {"user_id": user_id, "keep_count": keep_count})
                
                conn.commit()
                deleted_count = result.rowcount
                
                if deleted_count > 0:
                    print(f"🗑️ Cleaned up {deleted_count} old experiences for {user_id}")
                
                return deleted_count

        except Exception as e:
            print(f"❌ Failed to cleanup experiences: {e}")
            return 0

# Test the corrected memory manager
if __name__ == "__main__":
    print("🧪 Testing Corrected Memory Manager...")
    
    try:
        memory = MemoryManager()
        
        # Test basic storage
        basic_result = memory.store_experience(
            "test_user", 
            {"type": "test", "message": "Hello world"}, 
            {"mood": "positive"},
            0.7
        )
        print(f"✅ Basic storage: {'Success' if basic_result else 'Failed'}")
        
        # Test enhanced storage
        enhanced_result = memory.store_enhanced_experience(
            "test_user",
            {"type": "chat", "message": "I'm feeling stressed about work deadlines"},
            {"stress": 0.8, "anxiety": 0.6},
            0.7
        )
        print(f"✅ Enhanced storage: {'Success' if enhanced_result else 'Failed'}")
        
        # Test retrieval
        experiences = memory.retrieve_experiences("test_user", 5)
        print(f"✅ Retrieved: {len(experiences)} experiences")
        
        # Test statistics
        stats = memory.get_memory_statistics("test_user")
        print(f"✅ Statistics: {stats.get('total_experiences', 0)} total experiences")
        
        print("🎉 Memory Manager test complete!")
        
    except Exception as e:
        print(f"❌ Memory Manager test failed: {e}")
