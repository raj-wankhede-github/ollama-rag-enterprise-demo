"""
Script to test RAG functionality locally.
"""

import sys
import os
from src.config import config
from src.utils.logger import get_logger
from src.rag.pipeline import RAGPipeline

logger = get_logger(__name__, config.log_level)


def test_rag():
    """Test RAG pipeline"""
    logger.info("Testing RAG pipeline...")
    
    try:
        # Initialize pipeline
        pipeline = RAGPipeline()
        
        # Test query without ingested documents
        logger.info("Testing query with empty knowledge base...")
        result = pipeline.query("What is the meaning of life?")
        logger.info(f"Response: {result['response']}")
        
        # Create a test document
        logger.info("Creating test document...")
        test_doc_path = "./test_document.txt"
        with open(test_doc_path, "w") as f:
            f.write("""
            Artificial Intelligence is a branch of computer science that deals with creating intelligent agents.
            Machine Learning is a subset of AI that focuses on learning from data.
            Deep Learning uses neural networks with multiple layers.
            Natural Language Processing helps computers understand human language.
            Computer Vision enables computers to interpret visual information.
            """)
        
        # Ingest test document
        logger.info("Ingesting test document...")
        ingest_result = pipeline.ingest_document(test_doc_path)
        logger.info(f"Ingest result: {ingest_result}")
        
        # Test query with ingested document
        logger.info("Testing query with ingested document...")
        result = pipeline.query("What is Machine Learning?")
        logger.info(f"Query: What is Machine Learning?")
        logger.info(f"Response: {result['response']}")
        logger.info(f"Sources: {result['sources']}")
        
        # Clean up
        if os.path.exists(test_doc_path):
            os.remove(test_doc_path)
        
        logger.info("RAG testing completed successfully!")
        return True
    
    except Exception as e:
        logger.error(f"Error during RAG testing: {e}")
        return False


if __name__ == "__main__":
    success = test_rag()
    sys.exit(0 if success else 1)
