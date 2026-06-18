"""
FastAPI application for local development and testing.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
from ..config import config
from ..utils.logger import get_logger
from ..utils.storage import get_storage_provider
from ..rag.pipeline import RAGPipeline

logger = get_logger(__name__, config.log_level)


# Initialize FastAPI
app = FastAPI(
    title="Ollama RAG Enterprise Demo",
    description="RAG application using Ollama and Chroma",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
try:
    rag_pipeline = RAGPipeline()
except Exception as e:
    logger.error(f"Failed to initialize RAG pipeline: {e}")
    raise

# Initialize storage
storage = get_storage_provider(
    config.storage_type,
    bucket_name=config.aws_s3_bucket if config.is_aws() else None,
    base_dir=config.local_upload_dir
)


# Pydantic models
class QueryRequest(BaseModel):
    """Query request model"""
    query: str
    top_k: Optional[int] = config.top_k_results
    stream: Optional[bool] = False


class QueryResponse(BaseModel):
    """Query response model"""
    query: str
    response: str
    sources: List[dict]


class DocumentResponse(BaseModel):
    """Document ingestion response"""
    success: bool
    message: str
    document_count: Optional[int] = None
    error: Optional[str] = None


# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": config.environment,
        "ollama_available": rag_pipeline.llm.is_available()
    }


@app.get("/info")
async def info():
    """Application info endpoint"""
    return {
        "name": "Ollama RAG Enterprise Demo",
        "version": "1.0.0",
        "environment": config.environment,
        "ollama_model": config.ollama_model,
        "embedding_model": config.ollama_embedding_model,
        "vector_db": config.vector_db_type,
        "storage_type": config.storage_type,
        "supported_file_types": {
            "documents": [
                {"format": "PDF", "extension": ".pdf", "description": "PDF documents"},
                {"format": "CSV", "extension": ".csv", "description": "Comma-separated values"},
                {"format": "Excel 2007+", "extension": ".xlsx", "description": "Excel workbook"},
                {"format": "Excel 97-2003", "extension": ".xls", "description": "Legacy Excel workbook"},
                {"format": "Text", "extension": ".txt", "description": "Plain text files"},
                {"format": "Markdown", "extension": ".md, .markdown", "description": "Markdown files"}
            ]
        },
        "max_upload_size_mb": config.max_upload_size_mb
    }


@app.post("/ingest", response_model=DocumentResponse)
async def ingest_document(file: UploadFile = File(...)):
    """Ingest a document into the RAG system
    
    Supported file types:
    - PDF (.pdf)
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    - Text (.txt)
    - Markdown (.md, .markdown)
    """
    try:
        # Supported file extensions
        SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.csv', '.xlsx', '.xls', '.md', '.markdown'}
        
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )
        
        # Validate file size
        if file.size and file.size > config.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds {config.max_upload_size_mb}MB limit"
            )
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Upload to storage
            storage_key = f"documents/{file.filename}"
            if config.storage_type == "s3":
                storage.upload_file(tmp_path, storage_key)
            
            # Ingest into RAG
            result = rag_pipeline.ingest_document(tmp_path)
            
            return DocumentResponse(
                success=result["success"],
                message=result.get("message", ""),
                document_count=result.get("document_count"),
                error=result.get("error")
            )
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query(request: QueryRequest):
    """Query the RAG system"""
    try:
        if request.stream:
            # Stream response
            async def generate():
                for chunk in rag_pipeline.stream_response(
                    request.query,
                    rag_pipeline.retrieve(request.query, k=request.top_k)
                ):
                    yield chunk.encode()
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            # Non-streaming response
            result = rag_pipeline.query(request.query)
            return QueryResponse(
                query=result["query"],
                response=result["response"],
                sources=result["sources"]
            )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from the RAG system"""
    try:
        result = rag_pipeline.delete_documents([doc_id])
        return result
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ollama RAG Enterprise Demo API",
        "docs": "/docs",
        "health": "/health",
        "info": "/info"
    }
