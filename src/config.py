"""
Configuration management for Ollama RAG application.
Supports both local development and AWS Lambda deployment.
"""

import os
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class Environment(str, Enum):
    """Application environment types"""
    LOCAL = "local"
    AWS = "aws"
    DOCKER = "docker"


@dataclass
class Config:
    """Application configuration"""
    
    # Environment
    environment: str = os.getenv("ENV", "local")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Ollama Configuration
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "mistral")
    ollama_embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    
    # Vector Database Configuration
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "chroma")  # chroma, pinecone, weaviate
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
    
    # AWS Configuration
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_s3_bucket: str = os.getenv("AWS_S3_BUCKET", "")
    aws_dynamodb_table: str = os.getenv("AWS_DYNAMODB_TABLE", "rag-embeddings")
    
    # File Storage
    storage_type: str = os.getenv("STORAGE_TYPE", "local")  # local or s3
    local_upload_dir: str = os.getenv("LOCAL_UPLOAD_DIR", "./data/uploads")
    
    # API Configuration
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    
    # RAG Configuration
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    top_k_results: int = int(os.getenv("TOP_K_RESULTS", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
    
    # Database Configuration (for PostgreSQL with pgvector)
    database_url: Optional[str] = os.getenv("DATABASE_URL", None)
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_db: str = os.getenv("POSTGRES_DB", "rag_embeddings")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Request Configuration
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "300"))
    
    def is_aws(self) -> bool:
        """Check if running in AWS environment"""
        return self.environment.lower() == "aws"
    
    def is_local(self) -> bool:
        """Check if running locally"""
        return self.environment.lower() == "local"
    
    def validate(self) -> None:
        """Validate configuration"""
        if self.is_aws():
            if not self.aws_s3_bucket:
                raise ValueError("AWS_S3_BUCKET must be set in AWS environment")
        
        if self.vector_db_type == "pinecone":
            if not os.getenv("PINECONE_API_KEY"):
                raise ValueError("PINECONE_API_KEY must be set when using Pinecone")
        
        # Ensure upload directory exists for local storage
        if self.storage_type == "local" and self.is_local():
            os.makedirs(self.local_upload_dir, exist_ok=True)


# Global config instance
config = Config()
