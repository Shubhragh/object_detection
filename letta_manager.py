import requests
import json
from typing import Dict, Any, List
from config.settings import settings
from api_manager import APIManager

class LettaManager:
    def __init__(self):
        self.base_url = settings.LETTA_SERVER_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.api_manager = APIManager()
    
    def check_letta_connection(self) -> bool:
        """Check if Letta server is running"""
        try:
            response = self.session.get(f"{self.base_url}/v1/agents")
            return response.status_code in [200, 404]
        except Exception as e:
            print(f"❌ Cannot connect to Letta server: {e}")
            return False
    
    def create_agent(self, name: str, system_prompt: str, tools: List[str] = None, 
                    use_gemini: bool = True) -> Dict[str, Any]:
        """Create agent with all required Letta fields"""
        
        if not self.check_letta_connection():
            return self._create_agent_fallback(name, system_prompt, tools, use_gemini)
        
        if use_gemini:
            model_name = settings.GEMINI_MODEL
            embedding_model = settings.GEMINI_EMBEDDING
            embedding_dim = settings.GEMINI_EMBEDDING_DIM
            model_endpoint_type = "google_ai"
            embedding_endpoint_type = "google_ai"
        else:
            model_name = settings.GROQ_MODEL
            embedding_model = settings.GROQ_EMBEDDING
            embedding_dim = settings.GROQ_EMBEDDING_DIM
            model_endpoint_type = "groq"
            embedding_endpoint_type = "groq"
        
        print(f"🔄 Creating agent '{name}' with model: {model_name}, embedding: {embedding_model}")
        
        # Format that worked for Gemini (alternative format 1)
        payload = {
            "name": name,
            "system": system_prompt,
            "model": model_name,
            "model_endpoint_type": model_endpoint_type,
            "embedding_model": embedding_model,
            "embedding_endpoint_type": embedding_endpoint_type,
            "embedding_dim": embedding_dim,
            "context_window": settings.MEMORY_LIMIT,
            "tools": tools or []
        }
        
        try:
            response = self.session.post(f"{self.base_url}/v1/agents", json=payload)
            
            if response.status_code == 200:
                agent_data = response.json()
                print(f"✅ Created agent: {name} (ID: {agent_data.get('id')})")
                return agent_data
            else:
                print(f"❌ Direct format failed: {response.text}")
                return self._try_config_format(name, system_prompt, tools, use_gemini)
                
        except Exception as e:
            print(f"❌ Exception creating agent: {e}")
            return self._create_agent_fallback(name, system_prompt, tools, use_gemini)
    
    def _try_config_format(self, name: str, system_prompt: str, 
                          tools: List[str] = None, use_gemini: bool = True) -> Dict[str, Any]:
        """Try config object format with all required fields"""
        if use_gemini:
            model_name = settings.GEMINI_MODEL
            embedding_model = settings.GEMINI_EMBEDDING
            embedding_dim = settings.GEMINI_EMBEDDING_DIM
            model_endpoint_type = "google_ai"
            embedding_endpoint_type = "google_ai"
        else:
            model_name = settings.GROQ_MODEL
            embedding_model = settings.GROQ_EMBEDDING
            embedding_dim = settings.GROQ_EMBEDDING_DIM
            model_endpoint_type = "groq"
            embedding_endpoint_type = "groq"
        
        payload = {
            "name": name,
            "system": system_prompt,
            "llm_config": {
                "model": model_name,
                "model_endpoint_type": model_endpoint_type,
                "context_window": settings.MEMORY_LIMIT,
                "put_inner_thoughts_in_kwargs": True
            },
            "embedding_config": {
                "embedding_model": embedding_model,
                "embedding_endpoint_type": embedding_endpoint_type,
                "embedding_dim": embedding_dim
            },
            "tools": tools or []
        }
        
        try:
            print("🔄 Trying config format with all required fields...")
            response = self.session.post(f"{self.base_url}/v1/agents", json=payload)
            
            if response.status_code == 200:
                agent_data = response.json()
                print(f"✅ Created agent using config format: {name}")
                return agent_data
            else:
                print(f"❌ Config format failed: {response.text}")
                return self._create_agent_fallback(name, system_prompt, tools, use_gemini)
                
        except Exception as e:
            print(f"❌ Config format exception: {e}")
            return self._create_agent_fallback(name, system_prompt, tools, use_gemini)
    
    def _create_agent_fallback(self, name: str, system_prompt: str, 
                              tools: List[str] = None, use_gemini: bool = True) -> Dict[str, Any]:
        """Fallback agent creation using direct API calls"""
        print("🔄 Creating fallback agent using direct API...")
        
        test_response = self.api_manager.generate_response(
            f"You are {name}. {system_prompt}\n\nRespond briefly that you are ready to work.",
            use_gemini=use_gemini
        )
        
        agent_data = {
            "id": f"fallback_{name.lower().replace(' ', '')}_{abs(hash(name)) % 10000}",
            "name": name,
            "system_prompt": system_prompt,
            "model": settings.GEMINI_MODEL if use_gemini else settings.GROQ_MODEL,
            "test_response": test_response,
            "status": "active",
            "fallback_mode": True
        }
        
        print(f"✅ Created fallback agent: {name} (ID: {agent_data['id']})")
        return agent_data
    
    def send_message(self, agent_id: str, message: str, use_gemini: bool = True) -> Dict[str, Any]:
        """Send message using format that worked (format 2)"""
        if not self.check_letta_connection() or agent_id.startswith("fallback_"):
            return self._send_message_fallback(agent_id, message, use_gemini)
        
        print(f"📤 Sending message to agent {agent_id}: {message[:50]}...")
        
        # Format 2 that worked for Gemini
        payload = {
            "message": message,
            "role": "user"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/agents/{agent_id}/messages", 
                json=payload
            )
            
            if response.status_code == 200:
                response_data = response.json()
                print("✅ Message sent successfully via Letta")
                return response_data
            else:
                print(f"❌ Message failed: {response.status_code} - {response.text}")
                return self._try_alternative_message_formats(agent_id, message, use_gemini)
                
        except Exception as e:
            print(f"❌ Exception sending message: {e}")
            return self._send_message_fallback(agent_id, message, use_gemini)
    
    def _try_alternative_message_formats(self, agent_id: str, message: str, use_gemini: bool = True) -> Dict[str, Any]:
        """Try different message formats"""
        message_formats = [
            # Format with content field (what Letta seems to want)
            {
                "messages": [
                    {"role": "user", "content": message}
                ]
            },
            # Format with text field
            {
                "messages": [
                    {"role": "user", "text": message}
                ]
            },
            # Simple message format
            {"text": message, "role": "user"}
        ]
        
        for i, msg_payload in enumerate(message_formats):
            try:
                print(f"🔄 Trying message format {i+1}...")
                response = self.session.post(
                    f"{self.base_url}/v1/agents/{agent_id}/messages", 
                    json=msg_payload
                )
                
                if response.status_code == 200:
                    print(f"✅ Message sent successfully using format {i+1}")
                    return response.json()
                else:
                    print(f"❌ Format {i+1} failed: {response.text[:100]}...")
                    
            except Exception as e:
                continue
        
        print("❌ All message formats failed, using fallback")
        return self._send_message_fallback(agent_id, message, use_gemini)
    
    def _send_message_fallback(self, agent_id: str, message: str, use_gemini: bool = True) -> Dict[str, Any]:
        """Fallback message sending using direct API"""
        print("🔄 Using direct API fallback for message")
        api_response = self.api_manager.generate_response(message, use_gemini=use_gemini)
        
        return {
            "agent_id": agent_id,
            "message": message,
            "response": api_response,
            "timestamp": json.dumps({"timestamp": "now"}),
            "source": "direct_api"
        }
    
    def get_agent_memory(self, agent_id: str) -> Dict[str, Any]:
        """Get agent's memory state"""
        if not self.check_letta_connection() or agent_id.startswith("fallback_"):
            return {"memory": "fallback_memory", "agent_id": agent_id, "status": "fallback"}
        
        try:
            response = self.session.get(f"{self.base_url}/v1/agents/{agent_id}/memory")
            
            if response.status_code == 200:
                return response.json()
            else:
                # Memory endpoint might not exist for new agents
                return {"memory": "not_available", "agent_id": agent_id, "status": "standard"}
        except Exception as e:
            return {"memory": "error", "agent_id": agent_id, "status": "error", "error": str(e)}

# Complete test
if __name__ == "__main__":
    print("🧪 Complete Letta Manager Test")
    print("="*50)
    
    letta = LettaManager()
    
    # Test Gemini Agent
    print("\n🧪 Test 1: Create Gemini Agent")
    gemini_agent = letta.create_agent(
        name="GeminiTestAgent",
        system_prompt="You are a helpful assistant using Gemini 2.5 Flash. Be concise and confirm your identity.",
        use_gemini=True
    )
    
    if gemini_agent:
        print(f"✅ Gemini agent created: {gemini_agent['id']}")
        
        # Test message
        response = letta.send_message(
            gemini_agent['id'], 
            "Hello! Please confirm you're working with Gemini 2.5 Flash.", 
            use_gemini=True
        )
        print(f"Gemini Response: {response.get('response', 'No response')}")
    
    # Test Groq Agent with correct embedding
    print("\n🧪 Test 2: Create Groq Agent")
    groq_agent = letta.create_agent(
        name="GroqTestAgent",
        system_prompt="You are a helpful assistant using Llama-3.3-70B-Versatile. Be concise and confirm your identity.",
        use_gemini=False
    )
    
    if groq_agent:
        print(f"✅ Groq agent created: {groq_agent['id']}")
        
        # Test message
        response = letta.send_message(
            groq_agent['id'], 
            "Hello! Please confirm you're working with Llama 3.3 70B.", 
            use_gemini=False
        )
        print(f"Groq Response: {response.get('response', 'No response')[:200]}...")
    
    print("\n🎉 Testing complete!")
