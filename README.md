# Ollama RAG Enterprise Demo

A production-ready **Retrieval-Augmented Generation (RAG)** application using **Ollama** for local LLM inference. Designed to run locally and in Docker for development and deployment.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Local Development](#local-development)
- [How to Run Locally](#how-to-run-locally)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Database Choices](#database-choices)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Local RAG Pipeline** - Run everything locally using Ollama
- **Multiple File Types** - Support for TXT, PDF, and Markdown files
- **Vector Database** - Chroma for local embeddings (with Pinecone support)
- **FastAPI** - Modern, async REST API with automatic documentation
- **Docker Support** - Docker and Docker Compose for containerized deployment
- **Streaming Responses** - Real-time streaming of generated responses
- **Configuration Management** - Environment-based config for local/docker
- **Comprehensive Logging** - Built-in logging for debugging

---

## 🏗️ Architecture

### Local Development Flow
```
Document Upload → File Processing → Chunking → Embedding Generation → Vector Store (Chroma)
                                                                              ↓
Query Input → Query Embedding → Vector Search → Context Retrieval → LLM Generation (Ollama)
```


## 📦 Prerequisites

### Local Development
- **Python 3.9+**
- **Ollama** - Download from [ollama.ai](https://ollama.ai)
- **pip** or **conda**


## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ollama-rag-enterprise-demo.git
cd ollama-rag-enterprise-demo
```

### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n ollama-rag python=3.11
conda activate ollama-rag
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama
1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install and start the Ollama service
3. Pull the required models:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### Step 5: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

---

## 💻 Local Development

### Running the API Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

Access the API documentation at: `http://localhost:8000/docs`

### Configuration for Local Development

Edit `.env`:
```bash
ENV=local
DEBUG=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
STORAGE_TYPE=local
VECTOR_DB_TYPE=chroma
```

---

## 🎯 How to Run Locally

### 1. Start Ollama
```bash
# On Windows/Mac
# Ollama should auto-start as a service

# Or run manually (Linux)
ollama serve
```

Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

### 2. Prepare Your Documents

Place your documents in the `data/uploads` directory:
```
data/
├── uploads/
│   ├── document1.txt
│   ├── document2.pdf
│   └── document3.md
└── chroma_db/
```

### 3. Run the Application

```bash
# Terminal 1: Start FastAPI server
python main.py

# Terminal 2: Test the API (in another terminal)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

### 4. Use the API

**Upload a document:**
```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@data/uploads/mydocument.txt"
```

**Query the system:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "top_k": 5,
    "stream": false
  }'
```

**Check health:**
```bash
curl http://localhost:8000/health
```

---

## 📡 API Endpoints

### GET `/health`
Health check endpoint
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "environment": "local",
  "ollama_available": true
}
```

### GET `/info`
Application information
```bash
curl http://localhost:8000/info
```

### POST `/ingest`
Upload and ingest a document

**Request:**
```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@document.txt"
```

**Response:**
```json
{
  "success": true,
  "message": "Ingested 45 chunks",
  "document_count": 45
}
```

### POST `/query`
Query the RAG system

**Request:**
```json
{
  "query": "What is the document about?",
  "top_k": 5,
  "stream": false
}
```

**Response:**
```json
{
  "query": "What is the document about?",
  "response": "The document discusses...",
  "sources": [
    {
      "source": "document.txt",
      "chunk_index": 0
    }
  ]
}
```

### DELETE `/documents/{doc_id}`
Delete a document

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended for Local)

```bash
cd docker
docker-compose up
```

Access the API at: `http://localhost:8000`

**What gets started:**
- Ollama service
- RAG application
- Persistent volumes for data

### Custom Docker Build

```bash
docker build -f docker/Dockerfile -t ollama-rag .
docker run -p 8000:8000 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ollama-rag
```

---

## 🧪 Testing

### Run Automated Tests

```bash
python test_rag.py
```

This script:
1. Tests query with empty knowledge base
2. Creates a test document
3. Ingests the document
4. Queries with the ingested document
5. Verifies results

### Manual Testing

**Test 1: Upload Document**
```bash
echo "Machine Learning is a subset of AI" > test.txt
curl -X POST http://localhost:8000/ingest -F "file=@test.txt"
```

**Test 2: Query**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Machine Learning?"}'
```

**Test 3: Stream Response**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain AI", "stream": true}'
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | local | Environment: local, docker |
| `OLLAMA_BASE_URL` | http://localhost:11434 | Ollama service URL |
| `OLLAMA_MODEL` | mistral | LLM model name |
| `OLLAMA_EMBEDDING_MODEL` | nomic-embed-text | Embedding model name |
| `VECTOR_DB_TYPE` | chroma | Vector database: chroma, pinecone |
| `CHROMA_PERSIST_DIR` | ./data/chroma_db | Chroma database location |
| `STORAGE_TYPE` | local | Storage: local |
| `API_PORT` | 8000 | API server port |
| `CHUNK_SIZE` | 1000 | Document chunk size |
| `CHUNK_OVERLAP` | 200 | Chunk overlap size |
| `TOP_K_RESULTS` | 5 | Top K results for retrieval |
| `SIMILARITY_THRESHOLD` | 0.5 | Minimum similarity score |

### Database Configuration

The application supports **Chroma** as the vector database:

**Chroma (Recommended)**
- Embedded vector database
- No setup required
- Persistent storage in `./data/chroma_db`
- Perfect for local development and docker

**Why Chroma for this project:**
- ✅ No external dependencies
- ✅ Lightweight and easy to run locally
- ✅ Persistent storage support
- ✅ Fast similarity search
- ✅ Open source

**Future Support:**
- Pinecone (cloud vector database)
- PostgreSQL with pgvector extension

---

## 📁 Project Structure

```
ollama-rag-enterprise-demo/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py             # FastAPI application
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── pipeline.py        # Main RAG orchestrator
│   │   ├── embeddings.py      # Embedding generation
│   │   ├── vector_store.py    # Vector database interface
│   │   ├── document_processor.py  # Document processing
│   │   └── llm.py             # LLM interface (Ollama)
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging utilities
│       └── storage.py         # Storage abstraction (Local)
├── data/
│   ├── uploads/               # Local document uploads
│   └── chroma_db/             # Vector database storage
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   └── (test files)
├── main.py                    # Entry point for local server
├── test_rag.py               # RAG testing script
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment variables
└── README.md                 # This file
```

---

## 🗄️ Database Choices

### Vector Database: Chroma

**Why Chroma:**
- **Embedded**: Runs in-process, no separate server needed
- **Lightweight**: Great for local and docker environments
- **Persistent**: Stores embeddings locally
- **Fast**: DuckDB backend for efficient similarity search
- **Open Source**: Community-driven, transparent

**Alternatives Considered:**

| Database | Pros | Cons | Use Case |
|----------|------|------|----------|
| **Pinecone** | Fully managed, scalable | Paid service | Large-scale production |
| **Weaviate** | Open source, powerful | More complex setup | Enterprise deployments |
| **FAISS** | Fast, efficient | Requires rebuilding | Research/batch processing |
| **PostgreSQL + pgvector** | SQL + vectors | Extra infrastructure | Existing Postgres setups |

**Chroma is optimal for this demo because:**
1. No external services required
2. Works well in local and docker environments
3. Minimal operational overhead
4. Easy local development
5. Simple persistent local storage

---

## 🔧 Troubleshooting

### Issue: "Ollama not available"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Verify connection
python -c "from src.rag.llm import LLM; llm = LLM(); print('Connected!' if llm.is_available() else 'Not available')"
```

### Issue: Out of memory errors

**Solution:**
```bash
# Reduce chunk size in .env
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# Use smaller embedding model
OLLAMA_EMBEDDING_MODEL=all-minilm
```

### Issue: Slow query performance

**Solution:**
1. Increase `TOP_K_RESULTS` in `.env`
2. Lower `SIMILARITY_THRESHOLD` to get more results
3. Optimize chunk size for your document type
4. Use faster Ollama model

### Issue: CORS errors in browser

**Solution:**
Already configured in FastAPI app with `CORSMiddleware`:
```python
# Allows all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)

# For production, restrict origins:
allow_origins=["https://yourdomain.com"],
```

---

## 📝 Example Workflows

### Workflow 1: Document Ingestion and Query

```bash
# 1. Start the server
python main.py

# 2. Ingest a document
curl -X POST http://localhost:8000/ingest \
  -F "file=@path/to/document.txt"

# 3. Query the document
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic?"}'

# 4. Get the response
# Response includes the generated answer and source references
```

### Workflow 2: Docker Development

```bash
# 1. Navigate to docker directory
cd docker

# 2. Start services
docker-compose up

# 3. Wait for services to start (~30 seconds)

# 4. Ingest document
curl -X POST http://localhost:8000/ingest \
  -F "file=@../data/document.txt"

# 5. Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here"}'

# 6. Stop services
docker-compose down
```

---

## 📊 Performance Metrics

Approximate performance on local machine (Intel i7, 16GB RAM):

- **Document ingestion**: 100 pages → ~10 seconds
- **Query latency**: Retrieve + Generate → 5-15 seconds
- **Embedding generation**: Per 1000 tokens → 200ms
- **Vector search**: Top 5 results → 50ms
- **LLM inference**: Per query → 3-10 seconds

---

## 🚀 Next Steps

1. **Customize models**: Change `OLLAMA_MODEL` to suite your needs
2. **Implement authentication**: Add JWT tokens to API
3. **Add caching**: Implement Redis for query results
4. **Scale vector DB**: Switch to managed Pinecone for production
5. **Add monitoring**: Add runtime and request metrics
6. **Enable fine-tuning**: Create custom embeddings for your domain

---

## 📄 License

MIT License - Feel free to use this project for commercial or personal use.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 💬 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

## 🎓 Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Chroma Documentation](https://docs.trychroma.com)
- [RAG Explained](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)

---

**Made with ❤️ for AI builders**
