# Contribution Guidelines

Thank you for your interest in contributing to the Ollama RAG Enterprise Demo!

## How to Contribute

### Reporting Issues

- Check if the issue already exists
- Provide a clear description of the problem
- Include steps to reproduce
- Share error messages and logs
- Mention your environment (OS, Python version, Ollama version)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ollama-rag-enterprise-demo.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow Python PEP 8 style guide
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python test_rag.py
   pytest tests/
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: clear description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe what your change does
   - Link any related issues
   - Ensure all tests pass

## Code Style

- Use Python 3.9+ type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions and classes
- Follow existing code patterns

## Areas for Contribution

- [ ] Additional vector databases (Pinecone, Weaviate)
- [ ] Support for more document formats
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] Additional tests
- [ ] Documentation improvements
- [ ] UI/Dashboard
- [ ] Authentication system

## Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black pylint

# Run tests
pytest tests/

# Format code
black src/

# Lint code
pylint src/
```

## Questions?

Open an issue with the `question` label or start a discussion.

---

**Thank you for contributing!**
