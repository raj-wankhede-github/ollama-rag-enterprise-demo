# Quick Start Guide

Get up and running with Ollama RAG Enterprise Demo in 5 minutes!

## Prerequisites

- Python 3.9+
- Ollama (download from [ollama.ai](https://ollama.ai))
- Git

## Installation (Windows, Mac, Linux)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ollama-rag-enterprise-demo.git
cd ollama-rag-enterprise-demo
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env if needed (defaults work for local development)
```

### 5. Download Ollama Models
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 6. Start Ollama Service
```bash
# Windows/Mac: Ollama auto-starts

# Linux
ollama serve
```

### 7. Start RAG Application
```bash
python main.py
```

The API will be available at: **http://localhost:8000**

## Quick Test

### In a new terminal:

```bash
# Check health
curl http://localhost:8000/health

# Ingest a document
echo "Python is a programming language" > test.txt
curl -X POST http://localhost:8000/ingest -F "file=@test.txt"

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Python?"}'
```

## Access Documentation

Open in browser: http://localhost:8000/docs

This gives you interactive API documentation where you can test all endpoints!

## Using Docker

```bash
# One command to run everything
cd docker
docker-compose up

# In another terminal, test the same endpoints above
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Test the CLI: `python cli.py --help`
- Upload your own documents!

## Troubleshooting

**"Connection refused" error?**
- Make sure Ollama is running: `ollama serve`

**"Out of memory" error?**
- Reduce CHUNK_SIZE in .env: `CHUNK_SIZE=500`

**"Module not found" error?**
- Activate virtual environment: `source venv/bin/activate`

## Commands Cheat Sheet

```bash
# Development
python main.py                          # Start server
python test_rag.py                      # Test RAG pipeline
python cli.py query "Your question"     # CLI query
python cli.py ingest path/to/file       # CLI ingest

# Docker
docker-compose up                       # Start with Ollama
docker-compose down                     # Stop services
```

---

**Stuck? Check [README.md](README.md) or see [Troubleshooting](README.md#-troubleshooting) section**
