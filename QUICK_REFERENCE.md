# Supported File Formats - Quick Reference

## Answer: What file types can be uploaded?

Your `/ingest` endpoint now accepts **6 file formats**:

| Format | Extension | Status | Use Case |
|--------|-----------|--------|----------|
| **PDF** | `.pdf` | ✅ Supported | Documents, reports, papers |
| **CSV** | `.csv` | ✅ Supported | Tabular data, databases |
| **Excel 2007+** | `.xlsx` | ✅ Supported | Modern spreadsheets |
| **Excel 97-2003** | `.xls` | ✅ Supported | Legacy spreadsheets |
| **Text** | `.txt` | ✅ Supported | Plain text files |
| **Markdown** | `.md`, `.markdown` | ✅ Supported | Documentation |

---

## Quick Upload Examples

### Upload CSV
```bash
curl -X POST "http://localhost:8000/ingest" -F "file=@data.csv"
```

### Upload Excel
```bash
curl -X POST "http://localhost:8000/ingest" -F "file=@spreadsheet.xlsx"
```

### Upload PDF
```bash
curl -X POST "http://localhost:8000/ingest" -F "file=@document.pdf"
```

### Upload Text
```bash
curl -X POST "http://localhost:8000/ingest" -F "file=@document.txt"
```

---

## What Changed

### New Code Added
1. **CSV Processing** - `process_csv_file()` method
2. **Excel Processing** - `process_xlsx_file()` and `process_xls_file()` methods
3. **File Validation** - Type checking in `/ingest` endpoint
4. **Format Info** - Enhanced `/info` endpoint

### New Dependencies
- `openpyxl==3.1.2` - Excel 2007+ support
- `xlrd==2.0.1` - Excel 97-2003 support

### Documentation
- SUPPORTED_FILE_FORMATS.md (1000+ lines)
- FILE_UPLOAD_GUIDE.md (300+ lines)
- FILE_FORMAT_IMPLEMENTATION.md (400+ lines)
- MULTI_FORMAT_SUMMARY.md (300+ lines)

---

## Test It Now

### 1. Create sample files
```bash
python create_sample_files.py
```

### 2. Start server
```bash
python main.py
```

### 3. Upload samples
```bash
curl -X POST "http://localhost:8000/ingest" -F "file=@sample_data.csv"
curl -X POST "http://localhost:8000/ingest" -F "file=@sample_sales.xlsx"
curl -X POST "http://localhost:8000/ingest" -F "file=@sample_document.txt"
curl -X POST "http://localhost:8000/ingest" -F "file=@sample_guide.md"
```

### 4. Query
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here"}'
```

---

## Processing Details

### CSV Files
- **Input**: Headers in first row
- **Output**: Readable format with column mapping
- **Example**:
```
Employee: Alice Johnson | Department: Engineering | Salary: 120000
```

### Excel Files
- **Input**: Multiple sheets with data
- **Output**: All sheet data extracted
- **Example**:
```
Sheet: Sales
Date: 2024-01-01 | Product: Widget A | Amount: 1000
```

### PDF Files
- **Input**: PDF document
- **Output**: Page-by-page text extraction
- **Example**:
```
--- Page 1 ---
[Page content here]
```

### Text Files
- **Input**: Plain text
- **Output**: Chunked by size with overlap
- **Example**: Automatic semantic chunking

### Markdown Files
- **Input**: Markdown structured text
- **Output**: Header-aware intelligent chunking
- **Example**: Maintains structure for better context

---

## API Response Examples

### Success Response
```json
{
  "success": true,
  "message": "Ingested 42 chunks",
  "document_count": 42,
  "error": null
}
```

### Error: Unsupported Format
```json
{
  "detail": "Unsupported file type: .doc. Supported types: .csv, .md, .markdown, .pdf, .txt, .xls, .xlsx"
}
```

### Error: File Too Large
```json
{
  "detail": "File size exceeds 100MB limit"
}
```

---

## Check Supported Formats

```bash
curl "http://localhost:8000/info" | jq .supported_file_types
```

Response:
```json
{
  "documents": [
    {"format": "PDF", "extension": ".pdf", "description": "PDF documents"},
    {"format": "CSV", "extension": ".csv", "description": "Comma-separated values"},
    {"format": "Excel 2007+", "extension": ".xlsx", "description": "Excel workbook"},
    {"format": "Excel 97-2003", "extension": ".xls", "description": "Legacy Excel workbook"},
    {"format": "Text", "extension": ".txt", "description": "Plain text files"},
    {"format": "Markdown", "extension": ".md, .markdown", "description": "Markdown files"}
  ]
}
```

---

## Configuration

### File Size Limit
```python
# In src/config.py
max_upload_size_mb = 100  # Adjust as needed
```

### Chunk Parameters
```python
chunk_size = 500  # Characters per chunk
chunk_overlap = 50  # Overlap between chunks
```

---

## Supported by Each Format

| Feature | CSV | XLSX | XLS | TXT | PDF | MD |
|---------|-----|------|-----|-----|-----|-----|
| Multiple sheets | - | ✅ | ✅ | - | - | - |
| Headers preserved | ✅ | ✅ | ✅ | - | - | ✅ |
| Structure aware | - | - | - | - | - | ✅ |
| Large files (>50MB) | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ |

---

## Common Issues & Solutions

### "Unsupported file type"
→ Use one of: .pdf, .csv, .xlsx, .xls, .txt, .md, .markdown

### "File size exceeds limit"
→ Increase `max_upload_size_mb` in config or split file

### CSV shows no data
→ Ensure headers in first row, UTF-8 encoding

### Excel file not processing
→ Try .xlsx format, remove sheet protection, check if corrupted

---

## Files to Read

1. **SUPPORTED_FILE_FORMATS.md** - Full format specifications
2. **FILE_UPLOAD_GUIDE.md** - Upload examples and scripts
3. **FILE_FORMAT_IMPLEMENTATION.md** - Technical details
4. **MULTI_FORMAT_SUMMARY.md** - Complete overview

---

**Version**: 1.0.0  
**Status**: ✅ Complete and Tested  
**Last Updated**: 2026-06-18
