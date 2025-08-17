"""
Relationship Memory Network for AI Life Operating System
Tracks relationships with people, places, concepts with emotional context
"""

import json
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import sessionmaker
import uuid
import re

Base = declarative_base()

class RelationshipEntity(Base):
    __tablename__ = 'relationship_entities'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False)
    entity_name = Column(String(255), nullable=False)
    entity_type = Column(String(100), nullable=False)  # person, place, concept, topic
    
    # Core relationship data
    relationship_data = Column(JSONB, default={})
    interaction_history = Column(JSONB, default=[])
    emotional_associations = Column(JSONB, default={})
    
    # Relationship metrics
    relationship_strength = Column(Float, default=0.0)
    trust_level = Column(Float, default=0.5)
    familiarity = Column(Float, default=0.0)
    
    # Interaction tracking
    first_interaction = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    total_interactions = Column(Integer, default=0)
    positive_interactions = Column(Integer, default=0)
    negative_interactions = Column(Integer, default=0)
    
    # Context tags for better search
    context_tags = Column(JSONB, default=[])

class RelationshipMemoryNetwork:
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
        
        if memory_manager and hasattr(memory_manager, 'engine'):
            # Use existing engine from memory_manager
            self.engine = memory_manager.engine
            if hasattr(memory_manager, 'SessionLocal'):
                self.SessionLocal = memory_manager.SessionLocal
            else:
                # Create SessionLocal if memory_manager doesn't have it
                from sqlalchemy.orm import sessionmaker
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        else:
            # Create independent database connection
            from config.settings import settings
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            
            self.engine = create_engine(settings.POSTGRES_URL)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        print("🤝 Relationship Memory Network initialized")

    
    def extract_entities_from_message(self, message: str, user_id: str = "user") -> List[Dict[str, Any]]:
        """Extract people, places, concepts from message"""
        entities = []
        message_lower = message.lower()
        
        # Extract people (simple name detection)
        people_indicators = ['my boss', 'my manager', 'my colleague', 'my friend', 'my family', 'my partner', 'my spouse']
        for indicator in people_indicators:
            if indicator in message_lower:
                entity_name = indicator.replace('my ', '')
                entities.append({
                    'name': entity_name,
                    'type': 'person',
                    'context': self._extract_context_around_entity(message, indicator)
                })
        
        # Extract places
        place_indicators = ['office', 'home', 'work', 'gym', 'school', 'hospital', 'store', 'restaurant']
        for place in place_indicators:
            if place in message_lower:
                entities.append({
                    'name': place,
                    'type': 'place',
                    'context': self._extract_context_around_entity(message, place)
                })
        
        # Extract concepts/topics
        concept_indicators = {
            'work_project': ['project', 'assignment', 'task', 'deadline'],
            'health': ['exercise', 'diet', 'sleep', 'medical'],
            'learning': ['course', 'study', 'learn', 'education'],
            'technology': ['computer', 'app', 'software', 'phone'],
            'finance': ['money', 'budget', 'salary', 'expense']
        }
        
        for concept, keywords in concept_indicators.items():
            if any(keyword in message_lower for keyword in keywords):
                entities.append({
                    'name': concept,
                    'type': 'concept',
                    'context': self._extract_context_around_entity(message, keywords[0])
                })
        
        return entities
    
    def _extract_context_around_entity(self, message: str, entity: str, window: int = 20) -> str:
        """Extract context around entity mention"""
        try:
            start = max(0, message.lower().find(entity.lower()) - window)
            end = min(len(message), message.lower().find(entity.lower()) + len(entity) + window)
            return message[start:end].strip()
        except:
            return message[:50]  # Fallback to first 50 chars
    
    def update_relationship_from_interaction(self, user_id: str, message: str, emotional_context: Dict[str, Any] = None):
        """Update relationships based on user interaction"""
        entities = self.extract_entities_from_message(message, user_id)
        
        for entity in entities:
            self.add_or_update_relationship(
                user_id=user_id,
                entity_name=entity['name'],
                entity_type=entity['type'],
                interaction_data={
                    'message': message,
                    'context': entity['context'],
                    'timestamp': datetime.utcnow().isoformat(),
                    'emotional_context': emotional_context or {}
                },
                emotional_associations=emotional_context or {}
            )
    
    def add_or_update_relationship(self, user_id: str, entity_name: str, entity_type: str,
                                 interaction_data: Dict[str, Any],
                                 emotional_associations: Dict[str, Any] = None) -> bool:
        """Add or update relationship with comprehensive tracking"""
        session = self.SessionLocal()
        
        try:
            # Check if relationship exists
            relationship = session.query(RelationshipEntity).filter_by(
                user_id=user_id,
                entity_name=entity_name
            ).first()
            
            if relationship:
                # Update existing relationship
                relationship.interaction_history.append(interaction_data)
                relationship.total_interactions += 1
                relationship.last_interaction = datetime.utcnow()
                
                # Update emotional associations
                if emotional_associations:
                    current_emotions = relationship.emotional_associations or {}
                    for emotion, intensity in emotional_associations.items():
                        if emotion in current_emotions:
                            # Weighted average of emotions
                            current_emotions[emotion] = (current_emotions[emotion] + intensity) / 2
                        else:
                            current_emotions[emotion] = intensity
                    relationship.emotional_associations = current_emotions
                
                # Update relationship metrics
                relationship.familiarity = min(1.0, relationship.total_interactions / 20.0)
                
                # Determine if interaction was positive or negative
                if emotional_associations:
                    is_positive = any(emotion in ['positive', 'happy', 'excited', 'grateful'] 
                                    for emotion in emotional_associations.keys())
                    is_negative = any(emotion in ['stress', 'frustrated', 'angry', 'sad'] 
                                    for emotion in emotional_associations.keys())
                    
                    if is_positive:
                        relationship.positive_interactions += 1
                    elif is_negative:
                        relationship.negative_interactions += 1
                
                # Calculate relationship strength
                total_emotional_interactions = relationship.positive_interactions + relationship.negative_interactions
                if total_emotional_interactions > 0:
                    positivity_ratio = relationship.positive_interactions / total_emotional_interactions
                    relationship.relationship_strength = (relationship.familiarity * 0.6 + positivity_ratio * 0.4)
                else:
                    relationship.relationship_strength = relationship.familiarity * 0.5
                
                print(f"🔄 Updated relationship with {entity_name} (strength: {relationship.relationship_strength:.2f})")
                
            else:
                # Create new relationship
                new_relationship = RelationshipEntity(
                    user_id=user_id,
                    entity_name=entity_name,
                    entity_type=entity_type,
                    interaction_history=[interaction_data],
                    emotional_associations=emotional_associations or {},
                    relationship_strength=0.1,
                    familiarity=0.05,
                    trust_level=0.5,
                    total_interactions=1,
                    positive_interactions=1 if emotional_associations and any(e in ['positive', 'happy'] for e in emotional_associations.keys()) else 0,
                    negative_interactions=1 if emotional_associations and any(e in ['stress', 'negative'] for e in emotional_associations.keys()) else 0,
                    context_tags=self._generate_context_tags(interaction_data, emotional_associations)
                )
                
                session.add(new_relationship)
                print(f"🆕 Created new relationship with {entity_name}")
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Failed to update relationship: {e}")
            return False
        finally:
            session.close()
    
    def _generate_context_tags(self, interaction_data: Dict[str, Any], emotional_associations: Dict[str, Any] = None) -> List[str]:
        """Generate context tags for better relationship search"""
        tags = []
        
        # Add emotional tags
        if emotional_associations:
            for emotion in emotional_associations.keys():
                tags.append(f"emotion:{emotion}")
        
        # Add context-based tags
        message = interaction_data.get('message', '').lower()
        if 'work' in message:
            tags.append('context:work')
        if 'help' in message:
            tags.append('context:help')
        if 'problem' in message or 'issue' in message:
            tags.append('context:problem')
        if 'good' in message or 'great' in message:
            tags.append('context:positive')
        
        return tags
    
    def get_relationship(self, user_id: str, entity_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed relationship information"""
        session = self.SessionLocal()
        try:
            relationship = session.query(RelationshipEntity).filter_by(
                user_id=user_id,
                entity_name=entity_name
            ).first()
            
            if relationship:
                return {
                    "entity_name": relationship.entity_name,
                    "entity_type": relationship.entity_type,
                    "relationship_strength": relationship.relationship_strength,
                    "trust_level": relationship.trust_level,
                    "familiarity": relationship.familiarity,
                    "emotional_associations": relationship.emotional_associations,
                    "total_interactions": relationship.total_interactions,
                    "positive_interactions": relationship.positive_interactions,
                    "negative_interactions": relationship.negative_interactions,
                    "first_interaction": relationship.first_interaction.isoformat(),
                    "last_interaction": relationship.last_interaction.isoformat(),
                    "recent_interactions": relationship.interaction_history[-5:],  # Last 5
                    "context_tags": relationship.context_tags
                }
            return None
            
        except Exception as e:
            print(f"❌ Failed to get relationship: {e}")
            return None
        finally:
            session.close()
    
    def get_relationship_network(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive relationship network analysis"""
        session = self.SessionLocal()
        try:
            relationships = session.query(RelationshipEntity).filter_by(user_id=user_id).all()
            
            if not relationships:
                return {"total_relationships": 0, "network_health": "no_data"}
            
            # Analyze relationship network
            network_stats = {
                "total_relationships": len(relationships),
                "by_type": defaultdict(int),
                "by_strength": {"strong": 0, "moderate": 0, "weak": 0},
                "emotional_profile": defaultdict(float),
                "most_interacted": [],
                "relationship_trends": [],
                "network_health": "healthy"
            }
            
            total_strength = 0
            all_emotions = []
            
            for rel in relationships:
                # Count by type
                network_stats["by_type"][rel.entity_type] += 1
                
                # Count by strength
                if rel.relationship_strength > 0.7:
                    network_stats["by_strength"]["strong"] += 1
                elif rel.relationship_strength > 0.4:
                    network_stats["by_strength"]["moderate"] += 1
                else:
                    network_stats["by_strength"]["weak"] += 1
                
                total_strength += rel.relationship_strength
                
                # Collect emotional data
                if rel.emotional_associations:
                    all_emotions.extend(rel.emotional_associations.keys())
                
                # Track most interacted
                network_stats["most_interacted"].append({
                    "name": rel.entity_name,
                    "type": rel.entity_type,
                    "interactions": rel.total_interactions,
                    "strength": rel.relationship_strength
                })
            
            # Calculate network metrics
            network_stats["average_relationship_strength"] = total_strength / len(relationships)
            
            # Sort most interacted
            network_stats["most_interacted"].sort(key=lambda x: x["interactions"], reverse=True)
            network_stats["most_interacted"] = network_stats["most_interacted"][:5]
            
            # Emotional profile
            if all_emotions:
                emotion_counts = Counter(all_emotions)
                total_emotions = sum(emotion_counts.values())
                for emotion, count in emotion_counts.items():
                    network_stats["emotional_profile"][emotion] = count / total_emotions
            
            # Network health assessment
            strong_ratio = network_stats["by_strength"]["strong"] / len(relationships)
            if strong_ratio > 0.3:
                network_stats["network_health"] = "excellent"
            elif strong_ratio > 0.1:
                network_stats["network_health"] = "good"
            elif network_stats["average_relationship_strength"] > 0.3:
                network_stats["network_health"] = "developing"
            else:
                network_stats["network_health"] = "needs_attention"
            
            return dict(network_stats)
            
        except Exception as e:
            print(f"❌ Failed to analyze relationship network: {e}")
            return {"error": str(e)}
        finally:
            session.close()
    
    def get_relationship_insights(self, user_id: str) -> List[str]:
        """Generate insights about user's relationship patterns"""
        network = self.get_relationship_network(user_id)
        insights = []
        
        if network.get("total_relationships", 0) == 0:
            return ["Continue interacting to build relationship intelligence"]
        
        # Relationship quantity insights
        total = network["total_relationships"]
        if total > 10:
            insights.append(f"Rich relationship network with {total} tracked entities")
        elif total > 5:
            insights.append(f"Growing relationship awareness with {total} entities")
        else:
            insights.append(f"Building relationship context with {total} entities")
        
        # Relationship quality insights
        avg_strength = network.get("average_relationship_strength", 0)
        if avg_strength > 0.6:
            insights.append("Strong relationships with good emotional connections")
        elif avg_strength > 0.4:
            insights.append("Moderate relationship strength - continue building connections")
        else:
            insights.append("Early relationship development stage")
        
        # Emotional insights
        emotional_profile = network.get("emotional_profile", {})
        if "stress" in emotional_profile and emotional_profile["stress"] > 0.3:
            insights.append("Stress frequently associated with relationships - monitor for support needs")
        if "positive" in emotional_profile and emotional_profile["positive"] > 0.4:
            insights.append("Positive emotional associations with relationships")
        
        # Type distribution insights
        by_type = network.get("by_type", {})
        if by_type.get("person", 0) > by_type.get("concept", 0):
            insights.append("Person-focused relationship pattern")
        if by_type.get("concept", 0) > 3:
            insights.append("Strong conceptual relationship awareness")
        
        return insights[:4]  # Return top 4 insights

# Test relationship memory system
if __name__ == "__main__":
    print("🧪 Testing Relationship Memory Network...")
    
    # Initialize system
    relationship_network = RelationshipMemoryNetwork()
    
    # Test entity extraction
    test_message = "I'm stressed about my project deadline. My boss is being unreasonable and I need help with time management."
    entities = relationship_network.extract_entities_from_message(test_message)
    print(f"✅ Extracted {len(entities)} entities: {[e['name'] for e in entities]}")
    
    # Test relationship update
    relationship_network.update_relationship_from_interaction(
        "test_user",
        test_message,
        {"stress": 0.8, "seeking_help": 0.6}
    )
    
    # Test network analysis
    network = relationship_network.get_relationship_network("test_user")
    print(f"✅ Network analysis: {network.get('total_relationships', 0)} relationships")
    
    # Test insights
    insights = relationship_network.get_relationship_insights("test_user")
    print(f"✅ Generated {len(insights)} insights")
    
    print("🎉 Relationship Memory Network test complete!")
