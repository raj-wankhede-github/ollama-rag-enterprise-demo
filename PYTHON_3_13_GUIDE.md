# Python 3.13 Compatibility Guide

## Overview

The Ollama RAG Enterprise Demo has been updated to support **Python 3.13.8** with the latest compatible package versions.

## Python 3.13 Requirements

- **Python Version**: 3.13.8 (or 3.13.x)
- **Recommended**: Use virtual environment
- **Package Manager**: pip (included with Python)

## Updated Dependencies

All packages have been upgraded to versions compatible with Python 3.13:

| Package | Version | Notes |
|---------|---------|-------|
| fastapi | 0.115.15 | Latest stable FastAPI |
| uvicorn | 0.34.3 | ASGI server with standard extras |
| pydantic | 2.12.1 | Latest v2 with Python 3.13 support |
| pydantic-settings | 2.6.1 | Configuration management |
| requests | 2.32.4 | Latest HTTP library |
| chromadb | 0.5.11 | Latest stable (fixed NumPy 2.0 issue) |
| numpy | 1.26.4 | Compatible with Python 3.13 |
| boto3 | 1.39.23 | AWS SDK latest |
| botocore | 1.42.23 | AWS core latest |
| python-dotenv | 1.0.1 | Environment management |
| pypdf | 5.0.1 | Latest PDF processing |

## Setup Instructions

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
python setup.py

# This will:
# 1. Upgrade pip
# 2. Create virtual environment (if needed)
# 3. Install all dependencies
# 4. Verify installation
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python verify_installation.py
```

### Option 3: Docker (No Python Installation Needed)

```bash
# Docker handles Python 3.13 installation
cd docker
docker-compose up

# Verify at http://localhost:8000/health
```

## Verifying Your Installation

### Quick Check

```bash
python verify_installation.py
```

Expected output:
```
✓ Python version is 3.13+
✓ fastapi                0.115.15
✓ pydantic               2.12.1
✓ chromadb               0.5.11
✓ numpy                  1.26.4
... (more packages)
✓ All dependencies verified successfully!
```

### Detailed Check

```bash
# Check Python version
python --version  # Should show 3.13.x

# Check installed packages
pip list | grep -E "fastapi|pydantic|chromadb|numpy"
```

## Code Changes for Python 3.13 Compatibility

### 1. ChromaDB 0.5.11 Updates

**What changed**: ChromaDB now handles NumPy 2.0 compatibility internally.

**File**: `src/rag/vector_store.py`
- Added fallback for `PersistentClient` initialization
- Improved error handling for collection creation
- Compatible with both old and new Chroma API

```python
# Now supports both APIs
try:
    # Try new Chroma 0.5.x API
    self.client = chromadb.Client(settings)
except:
    # Fallback to new API
    self.client = chromadb.PersistentClient(path=self.persist_dir)
```

### 2. PyPDF 5.0.1 Updates

**What changed**: PyPDF 5.0+ has improved text extraction.

**File**: `src/rag/document_processor.py`
- Added null checks for extracted text
- Improved error handling for empty PDFs
- Better chunk filtering

```python
# Now handles edge cases better
extracted_text = page.extract_text()
if extracted_text:  # Only add non-empty text
    content += f"\n--- Page {page_num + 1} ---\n"
    content += extracted_text
```

### 3. Pydantic 2.12.1 (No Changes Required)

**What changed**: Improved performance and validation

**Status**: Your code already uses Pydantic v2 syntax ✓
- All BaseModel usage is compatible
- Type hints are compatible

## Known Issues & Solutions

### Issue 1: "Module not found" errors

**Symptom**: `ModuleNotFoundError` when running `python main.py`

**Solution**:
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Issue 2: "NumPy 2.0" errors

**Symptom**: `AttributeError: np.float_ was removed in NumPy 2.0`

**Solution**: Already fixed! The updated `requirements.txt` pins numpy to 1.26.4

```bash
# Verify numpy version
python -c "import numpy; print(numpy.__version__)"
# Should show: 1.26.4

# If not, reinstall:
pip install --upgrade -r requirements.txt
```

### Issue 3: ChromaDB initialization fails

**Symptom**: `AttributeError` or `ImportError` from chromadb

**Solution**:
```bash
# Clear old ChromaDB cache
rm -rf data/chroma_db

# Reinstall chromadb
pip install --force-reinstall chromadb==0.5.11

# Try again
python main.py
```

### Issue 4: "Permission denied" or other OS issues

**Symptom**: Access errors on Windows/Linux

**Solution**:
```bash
# Ensure you have write permissions
# Windows: Run Command Prompt as Administrator
# Linux/Mac: Use sudo if needed

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall everything
pip install --upgrade -r requirements.txt
```

## Running the Application

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Make sure Ollama is running
# Start it in another terminal or check if it's running:
ollama serve

# In a third terminal, start the app
python main.py

# Access at http://localhost:8000/docs
```

### Docker Development

```bash
cd docker
docker-compose up

# Ollama and RAG app start automatically
# Access at http://localhost:8000/docs
```

### Testing

```bash
# Quick test
python verify_installation.py

# Full RAG test
python test_rag.py

# CLI test
python cli.py query "What is machine learning?"
```

## Performance Tips for Python 3.13

Python 3.13 brings several performance improvements:

1. **Faster Startup**: ~10-15% improvement
2. **Better Memory Management**: ~5-10% improvement
3. **Async Improvements**: Better asyncio performance

These improvements mean:
- ✓ Faster API response times
- ✓ Lower memory usage
- ✓ Better Lambda cold start times

## Troubleshooting by Symptom

### "python: command not found"
```bash
# Make sure Python 3.13 is installed
# Download from https://www.python.org/downloads/

# Verify installation
python3 --version  # Try python3 instead of python
```

### Virtual environment issues
```bash
# Delete and recreate
rm -rf venv
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### Package installation hangs
```bash
# Try with no cache
pip install --no-cache-dir -r requirements.txt

# Or increase timeout
pip install --default-timeout=1000 -r requirements.txt
```

### ImportError: No module named X
```bash
# Make sure virtual environment is activated
which python  # Should show venv path

# Check if package is installed
pip list | grep <package_name>

# Reinstall if needed
pip install <package_name>==<version>
```

## Updating Packages in the Future

To safely update packages while maintaining compatibility:

```bash
# Never run bare update
# pip install --upgrade -r requirements.txt  ❌ (not safe)

# Instead, update specific packages with testing
pip install --upgrade chromadb==<new_version>
python verify_installation.py
python test_rag.py

# Update requirements.txt after successful testing
```

## Python Version Upgrade Path

If you need to upgrade from Python 3.12 to 3.13:

1. Install Python 3.13.8 (don't uninstall 3.12)
2. Create new virtual environment:
   ```bash
   /path/to/python3.13 -m venv venv_py313
   ```
3. Activate and test:
   ```bash
   source venv_py313/bin/activate
   python setup.py
   ```
4. Keep both versions until verified

## System Requirements

### Minimum
- Python 3.13.0+
- 2GB RAM
- 500MB disk space

### Recommended
- Python 3.13.8+ (latest patch)
- 8GB RAM
- 5GB disk space (includes Ollama models)

### For AWS Deployment
- Same as above, plus AWS CLI configured

## Getting Help

If you encounter issues:

1. **Check logs**:
   ```bash
   python main.py 2>&1 | tee app.log
   ```

2. **Run verification**:
   ```bash
   python verify_installation.py
   ```

3. **Check version compatibility**:
   ```bash
   python -c "import sys; print(f'Python {sys.version}')"
   pip list
   ```

4. **Review troubleshooting** section above

## Summary

✓ All packages updated to latest versions  
✓ Full Python 3.13 compatibility  
✓ Automated setup script provided  
✓ Verification tools included  
✓ Troubleshooting guide available

**Ready to use!** Run `python setup.py` to get started.
