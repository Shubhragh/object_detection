import redis
import json
import asyncio
import time
from typing import Dict, Any, Callable, List
from config.settings import settings

class EventManager:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.subscribers = {}
        self.running = False
    
    def publish_event(self, event_type: str, data: Dict[str, Any], source: str = "system"):
        """Publish an event to the event stream"""
        event = {
            "type": event_type,
            "data": data,
            "source": source,
            "timestamp": time.time()
        }
        
        try:
            self.redis_client.publish(settings.EVENT_STREAM_NAME, json.dumps(event))
            print(f"📡 Published event: {event_type} from {source}")
            return True
        except Exception as e:
            print(f"❌ Failed to publish event: {e}")
            return False
    
    def subscribe_to_events(self, callback: Callable[[Dict[str, Any]], None]):
        """Subscribe to events with a callback function"""
        def event_handler():
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(settings.EVENT_STREAM_NAME)
            
            print(f"🔔 Subscribed to events on {settings.EVENT_STREAM_NAME}")
            
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        event_data = json.loads(message['data'])
                        callback(event_data)
                    except Exception as e:
                        print(f"❌ Error processing event: {e}")
        
        return event_handler
    
    def start_internal_clock(self, interval_seconds: int = 300):
        """Start internal clock that emits periodic events"""
        def clock_tick():
            while self.running:
                self.publish_event(
                    "internal_clock_tick",
                    {"interval": interval_seconds},
                    "internal_clock"
                )
                time.sleep(interval_seconds)
        
        import threading
        self.running = True
        clock_thread = threading.Thread(target=clock_tick)
        clock_thread.daemon = True
        clock_thread.start()
        print(f"⏰ Internal clock started (interval: {interval_seconds}s)")
    
    def stop_internal_clock(self):
        """Stop the internal clock"""
        self.running = False
        print("⏹️ Internal clock stopped")

# Example event handlers
def handle_timeout_event(event_data: Dict[str, Any]):
    """Handle timeout events"""
    print(f"⏱️ Timeout event received: {event_data}")

def handle_clock_tick(event_data: Dict[str, Any]):
    """Handle internal clock tick"""
    print(f"⏰ Clock tick: {event_data['timestamp']}")

if __name__ == "__main__":
    # Test event system
    event_manager = EventManager()
    
    # Start internal clock
    event_manager.start_internal_clock(30)  # 30-second intervals for testing
    
    # Subscribe to events
    event_handler = event_manager.subscribe_to_events(handle_clock_tick)
    
    # Start event listener in a separate thread
    import threading
    listener_thread = threading.Thread(target=event_handler)
    listener_thread.daemon = True
    listener_thread.start()
    
    print("Event system running... Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_manager.stop_internal_clock()
        print("Event system stopped")
