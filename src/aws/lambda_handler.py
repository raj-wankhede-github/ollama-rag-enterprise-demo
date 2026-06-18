"""
AWS Lambda handler for serverless deployment.
"""

import json
import base64
import tempfile
import os
from typing import Dict, Any
from ..config import config, Environment
from ..utils.logger import get_logger
from ..utils.storage import get_storage_provider
from ..rag.pipeline import RAGPipeline

logger = get_logger(__name__)

# Initialize RAG pipeline
try:
    rag_pipeline = RAGPipeline()
except Exception as e:
    logger.error(f"Failed to initialize RAG pipeline: {e}")
    raise

# Initialize storage for AWS
if config.is_aws():
    storage = get_storage_provider(
        "s3",
        bucket_name=config.aws_s3_bucket,
        region=config.aws_region
    )


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function.
    
    Event structure for API Gateway:
    {
        "httpMethod": "POST" | "GET",
        "path": "/query" | "/ingest" | "/health",
        "body": "JSON string or base64 encoded",
        "headers": {...}
    }
    """
    try:
        logger.info(f"Lambda handler called with path: {event.get('path')}")
        
        http_method = event.get("httpMethod", "GET").upper()
        path = event.get("path", "/")
        
        # Parse request body if present
        body = None
        if event.get("body"):
            if event.get("isBase64Encoded"):
                body = json.loads(base64.b64decode(event["body"]))
            else:
                body = json.loads(event.get("body", "{}"))
        
        # Route request
        if path == "/health":
            return _health_check()
        
        elif path == "/info":
            return _info()
        
        elif path == "/query" and http_method == "POST":
            return _handle_query(body)
        
        elif path == "/ingest" and http_method == "POST":
            return _handle_ingest(event)
        
        else:
            return _error_response(404, "Not found")
    
    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}")
        return _error_response(500, str(e))


def _health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return _success_response({
        "status": "healthy",
        "environment": config.environment,
        "ollama_available": rag_pipeline.llm.is_available()
    })


def _info() -> Dict[str, Any]:
    """Application info endpoint"""
    return _success_response({
        "name": "Ollama RAG Enterprise Demo",
        "version": "1.0.0",
        "environment": config.environment,
        "ollama_model": config.ollama_model,
        "embedding_model": config.ollama_embedding_model,
        "vector_db": config.vector_db_type,
        "storage_type": config.storage_type
    })


def _handle_query(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle query request"""
    try:
        if not body or "query" not in body:
            return _error_response(400, "Query field is required")
        
        query = body["query"]
        top_k = body.get("top_k", config.top_k_results)
        
        logger.info(f"Processing query: {query[:100]}...")
        
        # Execute RAG query
        result = rag_pipeline.query(query)
        
        return _success_response({
            "query": result["query"],
            "response": result["response"],
            "sources": result["sources"]
        })
    
    except Exception as e:
        logger.error(f"Error handling query: {e}")
        return _error_response(500, str(e))


def _handle_ingest(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle document ingestion"""
    try:
        # Get file from event (for S3 trigger or multipart upload)
        if "Records" in event and len(event["Records"]) > 0:
            # S3 trigger
            return _handle_s3_ingest(event)
        else:
            # Direct file upload via API Gateway (base64 encoded)
            return _handle_direct_ingest(event)
    
    except Exception as e:
        logger.error(f"Error handling ingest: {e}")
        return _error_response(500, str(e))


def _handle_s3_ingest(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle S3 trigger for document ingestion"""
    try:
        for record in event.get("Records", []):
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]
            
            logger.info(f"Processing S3 file: s3://{bucket}/{key}")
            
            # Download from S3
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                storage.download_file(key, tmp.name)
                
                try:
                    # Ingest into RAG
                    result = rag_pipeline.ingest_document(tmp.name)
                    logger.info(f"Ingestion result: {result}")
                finally:
                    if os.path.exists(tmp.name):
                        os.remove(tmp.name)
        
        return _success_response({
            "message": "Documents ingested successfully",
            "record_count": len(event.get("Records", []))
        })
    
    except Exception as e:
        logger.error(f"Error in S3 ingest: {e}")
        return _error_response(500, str(e))


def _handle_direct_ingest(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle direct file upload"""
    try:
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
        
        if "file_content" not in body or "filename" not in body:
            return _error_response(400, "file_content and filename are required")
        
        file_content = body["file_content"]
        filename = body["filename"]
        
        # Decode base64 if necessary
        if isinstance(file_content, str):
            file_content = base64.b64decode(file_content)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        try:
            # Upload to storage if AWS
            if config.is_aws():
                storage.upload_file(tmp_path, f"documents/{filename}")
            
            # Ingest into RAG
            result = rag_pipeline.ingest_document(tmp_path)
            
            return _success_response({
                "success": result["success"],
                "message": result.get("message", ""),
                "document_count": result.get("document_count")
            })
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        logger.error(f"Error in direct ingest: {e}")
        return _error_response(500, str(e))


def _success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format success response"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data)
    }


def _error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Format error response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"error": message})
    }
