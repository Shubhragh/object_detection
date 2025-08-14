import google.generativeai as genai
from groq import Groq
import os
from typing import Dict, Any, List
from config.settings import settings

class APIManager:
    def __init__(self):
        # Configure Gemini
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Gemini API configured")
        else:
            print("❌ Gemini API key not found")
            self.gemini_model = None
        
        # Configure Groq
        if settings.GROQ_API_KEY:
            self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            print("✅ Groq API configured")
        else:
            print("❌ Groq API key not found")
            self.groq_client = None
    
    def generate_with_gemini(self, prompt: str, **kwargs) -> str:
        """Generate response using Gemini 2.5 Flash"""
        try:
            if not self.gemini_model:
                return "Error: Gemini not configured"
            
            generation_config = genai.types.GenerationConfig(
                temperature=kwargs.get('temperature', 0.7),
                max_output_tokens=kwargs.get('max_tokens', 2000),
                top_p=kwargs.get('top_p', 0.8),
                top_k=kwargs.get('top_k', 40)
            )
            
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return f"Gemini Error: {str(e)}"
    
    def generate_with_groq(self, prompt: str, **kwargs) -> str:
        """Generate response using Llama-3.3-70B-Versatile on Groq"""
        try:
            if not self.groq_client:
                return "Error: Groq not configured"
            
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2000),
                top_p=kwargs.get('top_p', 1),
                stream=False
            )
            
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            return f"Groq Error: {str(e)}"
    
    def generate_response(self, prompt: str, use_gemini: bool = True, **kwargs) -> str:
        """Generate response with fallback between APIs"""
        if use_gemini and self.gemini_model:
            response = self.generate_with_gemini(prompt, **kwargs)
            if "Error:" not in response:
                return response
            print("🔄 Falling back to Groq...")
        
        if self.groq_client:
            return self.generate_with_groq(prompt, **kwargs)
        
        return "Error: No working API available"

# Test the API manager
if __name__ == "__main__":
    api = APIManager()
    
    # Test Gemini 2.5 Flash
    print("Testing Gemini 2.5 Flash:")
    response = api.generate_with_gemini("Hello! Are you working properly? Please confirm you are Gemini 2.5 Flash.")
    print(f"Gemini response: {response}\n")
    
    # Test Llama-3.3-70B-Versatile
    print("Testing Llama-3.3-70B-Versatile on Groq:")
    response = api.generate_with_groq("Hello! Are you working properly? Please confirm you are Llama 3.3 70B.")
    print(f"Groq response: {response}")
