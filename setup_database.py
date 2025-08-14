import asyncio
import asyncpg
from sqlalchemy import create_engine, text
import redis
from config.settings import settings


async def setup_postgres():
    """Setup PostgreSQL database and tables"""
    
    # Connect using the credentials from your Docker container
    conn = await asyncpg.connect(
        host="localhost",
        user="aiuser",        # ✅ Match your Docker setup
        password="aipass",    # ✅ Match your Docker setup  
        database="postgres"   # Connect to default DB first
    )
    
    try:
        await conn.execute("CREATE DATABASE ailifeos")
        print("✅ Database 'ailifeos' created")
    except Exception as e:
        print(f"Database might already exist: {e}")
    finally:
        await conn.close()
    
    # Now connect to our database and create tables
    engine = create_engine(settings.POSTGRES_URL)
    
    with engine.connect() as conn:
        # Note: aiuser already exists in your Docker setup, so skip user creation
        # or handle the exception gracefully
        try:
            conn.execute(text("GRANT ALL PRIVILEGES ON DATABASE ailifeos TO aiuser"))
            print("✅ Granted privileges to aiuser")
        except Exception as e:
            print(f"Privileges might already be set: {e}")
        
        # Create basic tables
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS agent_states (
                id SERIAL PRIMARY KEY,
                agent_id VARCHAR(255) UNIQUE NOT NULL,
                agent_name VARCHAR(255) NOT NULL,
                current_state JSONB,
                last_updated TIMESTAMP DEFAULT NOW()
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS memory_experiences (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                experience_data JSONB,
                emotional_context JSONB,
                timestamp TIMESTAMP DEFAULT NOW(),
                importance_score FLOAT DEFAULT 0.5
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS event_log (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(255),
                event_data JSONB,
                source_agent VARCHAR(255),
                timestamp TIMESTAMP DEFAULT NOW()
            )
        """))
        
        conn.commit()
        print("✅ Database tables created")


def setup_redis():
    """Test Redis connection"""
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        print("✅ Redis connection successful")
        return r
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(setup_postgres())
    setup_redis()
