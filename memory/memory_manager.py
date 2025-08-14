import json
import time
from typing import Dict, Any, List
from sqlalchemy import create_engine, text
from config.settings import settings

class MemoryManager:
    def __init__(self):
        self.engine = create_engine(settings.POSTGRES_URL)
        
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

# Test it
if __name__ == "__main__":
    memory = MemoryManager()
    
    # Simple test
    memory.store_experience("test_user", {"message": "hello"}, {"mood": "happy"})
    experiences = memory.retrieve_experiences("test_user")
    print(f"✅ Memory manager working: {len(experiences)} experiences")
