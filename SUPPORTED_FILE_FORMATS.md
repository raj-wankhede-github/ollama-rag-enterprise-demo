# Supported File Formats for Document Ingestion

This document describes all file formats supported by the Ollama RAG Enterprise Demo for ingestion into the vector database.

## Overview

The `/ingest` endpoint accepts and processes the following file formats:

| Format | Extension | Description | Status |
|--------|-----------|-------------|--------|
| PDF | `.pdf` | Adobe Portable Document Format | ✅ Supported |
| CSV | `.csv` | Comma-Separated Values | ✅ Supported |
| Excel 2007+ | `.xlsx` | Microsoft Excel workbook | ✅ Supported |
| Excel 97-2003 | `.xls` | Legacy Excel workbook | ✅ Supported |
| Plain Text | `.txt` | Text files | ✅ Supported |
| Markdown | `.md`, `.markdown` | Markdown formatted text | ✅ Supported |

## File Specifications

### 1. PDF Files (`.pdf`)

**Processing Method**: Page-by-page text extraction

**Features**:
- Extracts text from all pages
- Preserves page numbers in metadata
- Automatically chunks large documents
- Handles scanned PDFs with text (OCR not supported)

**Limitations**:
- Scanned PDFs without OCR will not be processed
- Complex layouts may lose formatting
- Requires PyPDF library (included)

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"
```

**Processing Output**:
```json
{
  "success": true,
  "message": "Ingested 45 chunks",
  "document_count": 45
}
```

---

### 2. CSV Files (`.csv`)

**Processing Method**: Row-by-row conversion with header mapping

**Features**:
- Reads CSV with headers
- Maps each column name to its values
- Creates readable text format: `ColumnName: value | OtherColumn: value`
- Preserves data relationships
- Handles missing values gracefully

**CSV Requirements**:
- Must have a header row
- Can have up to 1000s of rows
- Supports UTF-8 encoding
- Standard comma-separated format

**Example CSV File**:
```csv
Name,Department,Salary,Experience
John Doe,Engineering,120000,5
Jane Smith,Marketing,95000,3
Bob Johnson,Sales,85000,4
```

**Processing Output**:
```
CSV Headers: Name | Department | Salary | Experience

Name: John Doe | Department: Engineering | Salary: 120000 | Experience: 5
Name: Jane Smith | Department: Marketing | Salary: 95000 | Experience: 3
Name: Bob Johnson | Department: Sales | Salary: 85000 | Experience: 4
```

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@data.csv"
```

---

### 3. Excel Files (`.xlsx`)

**Processing Method**: Sheet-by-sheet row extraction

**Features**:
- Handles multiple sheets
- Extracts all sheet data
- Preserves header information
- Handles various Excel data types (numbers, dates, text)
- Uses openpyxl library (included)

**Supported Features**:
- Multiple worksheets
- Data with headers
- Numbers, dates, and text values
- Up to 1 million rows per sheet

**Limitations**:
- Formulas are evaluated at read time
- Charts and images are not extracted
- Complex formatting is not preserved

**Example Excel File**:
```
Sheet: Sales Data
Headers: Date | Product | Amount | Region

Date: 2024-01-01 | Product: Widget A | Amount: 1000 | Region: North
Date: 2024-01-02 | Product: Widget B | Amount: 1500 | Region: South
```

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@sales_report.xlsx"
```

---

### 4. Excel Files (`.xls`)

**Processing Method**: Legacy Excel sheet-by-sheet extraction

**Features**:
- Supports Excel 97-2003 format
- Multiple sheet handling
- Row and column extraction
- Date and number formatting awareness

**Differences from XLSX**:
- Older Excel format (.xls)
- Same processing logic as `.xlsx`
- Used for legacy Excel files

**Compatibility**:
- Excel 97, 2000, XP, 2003
- Uses xlrd library (included)

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@legacy_data.xls"
```

---

### 5. Plain Text Files (`.txt`)

**Processing Method**: Direct text chunking

**Features**:
- Reads UTF-8 encoded text
- Simple text processing
- No special formatting required
- Default for unknown formats

**Encoding**:
- UTF-8 (recommended)
- ASCII compatible
- Fallback encoding: UTF-8 with error handling

**File Size**:
- Recommended: < 100MB
- Maximum configurable limit

**Example Text File**:
```
Introduction to Machine Learning

Machine learning is a subset of artificial intelligence
that focuses on the development of computer programs
that can learn and improve from experience.

Key Concepts:
- Supervised Learning
- Unsupervised Learning
- Reinforcement Learning
```

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.txt"
```

---

### 6. Markdown Files (`.md`, `.markdown`)

**Processing Method**: Header-aware chunking

**Features**:
- Preserves markdown structure
- Intelligently chunks by headers
- Maintains text hierarchy
- Better context preservation than plain text

**Markdown Support**:
- Headers: `# ## ### #### ##### ######`
- Code blocks
- Lists and formatting
- Links and references

**Processing Logic**:
- Chunks by header boundaries when possible
- Respects chunk size limits
- Maintains semantic context

**Example Markdown File**:
```markdown
# Project Documentation

## Overview
This project implements a RAG system.

### Architecture
The system consists of several components...

## Installation
To install the system:
```bash
pip install -r requirements.txt
```
"

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@README.md"
```

---

## Document Processing Pipeline

All uploaded files go through the following processing steps:

### 1. **Validation**
```
✓ File extension check
✓ File size validation
✓ Format verification
```

### 2. **Processing**
```
✓ Format-specific parsing
✓ Content extraction
✓ Text normalization
```

### 3. **Chunking**
```
✓ Split into semantic chunks
✓ Overlap for context
✓ Generate chunk IDs
```

### 4. **Embedding**
```
✓ Generate embeddings for each chunk
✓ Create vector representations
✓ Store in vector database
```

### 5. **Indexing**
```
✓ Index in Chroma
✓ Add metadata
✓ Link to source file
```

## Configuration

### Maximum File Size
```python
config.max_upload_size_mb = 100  # Default: 100MB
```

### Chunk Size
```python
config.chunk_size = 500  # Characters per chunk
config.chunk_overlap = 50  # Overlap between chunks
```

### Supported Extensions
```python
SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.csv', '.xlsx', '.xls', '.md', '.markdown'}
```

## API Endpoint Details

### POST `/ingest`

**Request**:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"
```

**Response Success** (200):
```json
{
  "success": true,
  "message": "Ingested 42 chunks",
  "document_count": 42,
  "error": null
}
```

**Response Error - Unsupported Format** (400):
```json
{
  "detail": "Unsupported file type: .doc. Supported types: .csv, .md, .markdown, .pdf, .txt, .xls, .xlsx"
}
```

**Response Error - File Too Large** (413):
```json
{
  "detail": "File size exceeds 100MB limit"
}
```

**Response Error - Processing Failed** (500):
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Query Information Endpoint

### GET `/info`

Returns supported file types and configuration:

```bash
curl "http://localhost:8000/info"
```

**Response**:
```json
{
  "name": "Ollama RAG Enterprise Demo",
  "version": "1.0.0",
  "supported_file_types": {
    "documents": [
      {
        "format": "PDF",
        "extension": ".pdf",
        "description": "PDF documents"
      },
      {
        "format": "CSV",
        "extension": ".csv",
        "description": "Comma-separated values"
      },
      // ... other formats
    ]
  },
  "max_upload_size_mb": 100
}
```

## Processing Examples

### Example 1: Ingest a PDF Report

```bash
# Upload PDF file
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@annual_report.pdf"

# Response
# {
#   "success": true,
#   "message": "Ingested 128 chunks",
#   "document_count": 128
# }

# Now query it
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What were the revenue figures?"}'
```

### Example 2: Ingest CSV Data

```bash
# Upload CSV file
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@sales_data.csv"

# Query the data
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What sales occurred in Q3?"}'
```

### Example 3: Ingest Excel Spreadsheet

```bash
# Upload Excel file
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@employee_database.xlsx"

# Query the data
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "List employees in the Engineering department"}'
```

## Troubleshooting

### Issue: "Unsupported file type"
- **Cause**: File extension not in supported list
- **Solution**: Convert to supported format or rename file with correct extension

### Issue: "File size exceeds limit"
- **Cause**: File is larger than `max_upload_size_mb`
- **Solution**: Split file into smaller chunks or increase limit in config

### Issue: "Failed to process document"
- **Cause**: File format corruption or invalid content
- **Solution**: 
  - Verify file is not corrupted
  - Try opening in native application
  - Check file encoding (UTF-8 for text files)

### Issue: CSV shows no data
- **Cause**: CSV file missing headers or has encoding issues
- **Solution**: 
  - Ensure first row contains column headers
  - Save CSV as UTF-8 encoded
  - Check for special characters

### Issue: Excel file not processing
- **Cause**: File format not recognized or contains protected sheets
- **Solution**: 
  - Save as `.xlsx` (2007+) instead of `.xls` if possible
  - Remove sheet protection
  - Verify file not corrupted

## Performance Characteristics

| Format | Processing Speed | Max File Size | Notes |
|--------|------------------|---------------|-------|
| TXT | Very fast | 100MB | Direct text reading |
| PDF | Medium | 100MB | Page extraction overhead |
| CSV | Fast | 100MB | Row-by-row processing |
| XLSX | Medium-Slow | 100MB | Cell-by-cell extraction |
| XLS | Medium-Slow | 100MB | Legacy format overhead |
| MD | Fast | 100MB | Header-aware chunking |

## Best Practices

1. **Use Appropriate Format**
   - Tabular data: Use CSV or Excel
   - Documents: Use PDF
   - Code/configs: Use Markdown or Text

2. **File Organization**
   - Keep files under 50MB for faster processing
   - Use consistent naming conventions
   - Store original files separately

3. **CSV Best Practices**
   - Include descriptive column headers
   - Ensure consistent data types per column
   - Use UTF-8 encoding
   - Avoid special characters in headers

4. **Excel Best Practices**
   - Put data in first sheet or clearly name sheets
   - Include headers in row 1
   - Use consistent formatting
   - Avoid merged cells if possible

5. **PDF Best Practices**
   - Ensure text is extractable (not scanned images)
   - Use standard fonts
   - Avoid heavily encrypted PDFs
   - Include proper metadata

## Future Format Support

Planned additions:
- [ ] Word documents (.docx)
- [ ] PowerPoint presentations (.pptx)
- [ ] JSON/JSONL files
- [ ] XML files
- [ ] Web page HTML

---

## Related Documentation

- [README.md](README.md) - Main documentation
- [API_DOCUMENTATION.md](README.md#api-endpoints) - API endpoints
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide

---

**Last Updated**: 2026-06-18  
**Version**: 1.0.0
