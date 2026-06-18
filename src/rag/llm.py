"""
LLM interface for Ollama.
"""

import requests
from typing import Generator
from ..utils.logger import get_logger
from ..config import config

logger = get_logger(__name__)


class OllamaLLM:
    """Interface for Ollama language model"""
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or config.ollama_base_url
        self.model = model or config.ollama_model
    
    def generate(self, prompt: str, stream: bool = False, **kwargs) -> str:
        """Generate text from prompt"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=config.request_timeout_seconds,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        import json
                        chunk = json.loads(line)
                        full_response += chunk.get("response", "")
                return full_response
            else:
                import json
                result = response.json()
                return result.get("response", "")
        except Exception as e:
            logger.error(f"Error generating text from Ollama: {e}")
            raise
    
    def generate_stream(self, prompt: str, **kwargs) -> Generator:
        """Generate text from prompt as a stream"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=config.request_timeout_seconds,
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    yield chunk.get("response", "")
        except Exception as e:
            logger.error(f"Error streaming from Ollama: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False
    
    def list_models(self) -> list:
        """List available models in Ollama"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []


class LLM:
    """Generic LLM wrapper"""
    
    def __init__(self, provider: str = "ollama", **kwargs):
        if provider == "ollama":
            self.llm = OllamaLLM(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def generate(self, prompt: str, stream: bool = False, **kwargs) -> str:
        """Generate text from prompt"""
        return self.llm.generate(prompt, stream=stream, **kwargs)
    
    def stream(self, prompt: str, **kwargs) -> Generator:
        """Stream text generation"""
        return self.llm.generate_stream(prompt, **kwargs)
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.llm.is_available()
