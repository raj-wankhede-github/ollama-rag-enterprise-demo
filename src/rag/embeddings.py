"""
Embedding models using Ollama or other providers.
"""

import requests
from typing import List
from ..utils.logger import get_logger
from ..config import config

logger = get_logger(__name__)


class OllamaEmbeddings:
    """Ollama embeddings provider"""
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or config.ollama_base_url
        self.model = model or config.ollama_embedding_model
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=config.request_timeout_seconds
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            try:
                embedding = self.embed_text(text)
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Error embedding text: {e}")
                embeddings.append([])  # Return empty embedding on error
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        try:
            embedding = self.embed_text("test")
            return len(embedding)
        except Exception as e:
            logger.error(f"Error getting embedding dimension: {e}")
            return 384  # Default for nomic-embed-text


class EmbeddingModel:
    """Generic embedding model wrapper"""
    
    def __init__(self, model_type: str = "ollama", **kwargs):
        if model_type == "ollama":
            self.model = OllamaEmbeddings(**kwargs)
        else:
            raise ValueError(f"Unsupported embedding model type: {model_type}")
    
    def embed(self, text: str) -> List[float]:
        """Embed a single text"""
        return self.model.embed_text(text)
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts"""
        return self.model.embed_texts(texts)
