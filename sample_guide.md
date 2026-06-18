# Getting Started with RAG Systems

## What is RAG?

RAG (Retrieval-Augmented Generation) combines:
- **Retrieval**: Finding relevant documents
- **Augmentation**: Using retrieved documents as context
- **Generation**: Creating responses with additional context

## Architecture Components

### 1. Document Processing
- Extract text from various formats
- Split into chunks
- Generate embeddings

### 2. Vector Database
- Store embeddings
- Perform similarity search
- Retrieve relevant chunks

### 3. Language Model
- Generate responses
- Use retrieved context
- Provide answers with sources

## Supported File Types

| Format | Extension | Purpose |
|--------|-----------|---------|
| PDF | .pdf | Documents |
| CSV | .csv | Tabular data |
| XLSX | .xlsx | Spreadsheets |
| TXT | .txt | Text files |
| MD | .md | Documentation |

## Quick Start

1. **Upload Documents**
   ```bash
   curl -X POST "http://localhost:8000/ingest" -F "file=@document.pdf"
   ```

2. **Query System**
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the main topic?"}'
   ```

3. **Get Results**
   - Response includes answer
   - Sources show where information came from
   - Confidence scores indicate relevance

## Benefits

✓ Access to document-specific information
✓ Better context for responses
✓ Reduced hallucinations
✓ Traceable sources
✓ Real-time document updates
