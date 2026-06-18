# Quick File Upload Guide

## Supported File Types

Your RAG application now supports uploading and ingesting the following file formats:

| Format | Extension | Use Case |
|--------|-----------|----------|
| **PDF** | `.pdf` | Documents, reports, whitepapers |
| **CSV** | `.csv` | Tabular data, databases, spreadsheets |
| **Excel** | `.xlsx` | Spreadsheets, workbooks (2007+) |
| **Excel** | `.xls` | Legacy spreadsheets (97-2003) |
| **Text** | `.txt` | Plain text files |
| **Markdown** | `.md, .markdown` | Documentation, notes |

## How to Upload Files

### Using cURL

```bash
# Upload a PDF
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"

# Upload a CSV
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@data.csv"

# Upload an Excel file
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@spreadsheet.xlsx"
```

### Using Python

```python
import requests

# Upload file
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/ingest", files=files)
    print(response.json())

# Response example:
# {
#   "success": true,
#   "message": "Ingested 42 chunks",
#   "document_count": 42
# }
```

### Using JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("http://localhost:8000/ingest", {
  method: "POST",
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Using FastAPI Docs UI

1. Start the server: `python main.py`
2. Open: http://localhost:8000/docs
3. Find the `/ingest` endpoint
4. Click "Try it out"
5. Click "Choose File"
6. Select your file
7. Click "Execute"

## Example: Processing Different File Types

### Example 1: PDF Document

```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@research_paper.pdf"

# Response:
# {
#   "success": true,
#   "message": "Ingested 156 chunks",
#   "document_count": 156
# }
```

### Example 2: CSV Data

Create `sales_data.csv`:
```csv
Date,Product,Amount,Region
2024-01-01,Widget A,1000,North
2024-01-02,Widget B,1500,South
2024-01-03,Widget A,2000,East
```

Upload:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@sales_data.csv"
```

Then query:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What was the total sales amount?"}'
```

### Example 3: Excel Spreadsheet

Create `employee_data.xlsx` with data:
- Sheet 1: Employee list (Name, Department, Salary)
- Sheet 2: Projects (Project, Team, Status)

Upload:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@employee_data.xlsx"
```

Query:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "List employees in Engineering department"}'
```

### Example 4: Markdown Documentation

Create `API_DOCS.md`:
```markdown
# API Documentation

## Endpoints

### GET /health
Returns system health status.

### POST /ingest
Accepts file uploads for ingestion.

### POST /query
Query the RAG system.
```

Upload:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@API_DOCS.md"
```

## Check Supported Formats

Get info about supported formats:

```bash
curl "http://localhost:8000/info"
```

Response includes:
```json
{
  "supported_file_types": {
    "documents": [
      {
        "format": "PDF",
        "extension": ".pdf",
        "description": "PDF documents"
      },
      ...
    ]
  },
  "max_upload_size_mb": 100
}
```

## File Size Limits

- **Default Maximum**: 100MB per file
- **Configurable**: Via `config.max_upload_size_mb`

To change:
```python
# In src/config.py
max_upload_size_mb = 200  # Set to 200MB
```

## Error Handling

### Unsupported File Type
```json
{
  "detail": "Unsupported file type: .doc. Supported types: .csv, .md, .markdown, .pdf, .txt, .xls, .xlsx"
}
```

**Solution**: Use one of the supported formats listed

### File Too Large
```json
{
  "detail": "File size exceeds 100MB limit"
}
```

**Solution**: Upload smaller file or increase limit in config

### Processing Error
```json
{
  "detail": "Error message..."
}
```

**Solution**: Check:
- File is not corrupted
- File is properly formatted
- File encoding is UTF-8 (for text files)

## Processing Workflow

```
┌─────────────────┐
│  Upload File    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validate File  │ ─► Check extension, size
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Process File   │ ─► Extract content based on type
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chunk Text     │ ─► Split into semantic chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate IDs   │ ─► Create unique identifiers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Store in DB    │ ─► Add to vector database
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ready to Query │
└─────────────────┘
```

## Tips for Best Results

1. **CSV Files**
   - ✓ Include column headers in first row
   - ✓ Use UTF-8 encoding
   - ✓ Avoid special characters in headers

2. **Excel Files**
   - ✓ Put data in the first sheet
   - ✓ Include headers
   - ✓ Avoid merged cells
   - ✓ Use `.xlsx` format (newer Excel)

3. **PDF Files**
   - ✓ Ensure text is selectable (not scanned image)
   - ✓ Use standard fonts
   - ✓ Avoid heavy encryption

4. **Text Files**
   - ✓ Save as UTF-8 encoded
   - ✓ Use .txt or .md extensions
   - ✓ Include clear structure (headings, sections)

## CLI Usage

```bash
# Using Python CLI (if available)
python cli.py ingest document.pdf
python cli.py ingest data.csv
python cli.py ingest spreadsheet.xlsx

# Then query
python cli.py query "What is the main topic?"
```

## Batch Upload

Upload multiple files:

```bash
# Shell script to upload all PDFs
for file in *.pdf; do
  curl -X POST "http://localhost:8000/ingest" \
    -F "file=@$file"
  echo "Uploaded $file"
done
```

Python:
```python
import os
import requests

for filename in os.listdir("documents/"):
    filepath = os.path.join("documents/", filename)
    with open(filepath, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/ingest", files=files)
        print(f"{filename}: {response.json()['message']}")
```

## Next Steps

1. **Upload Documents**: Use `/ingest` endpoint
2. **Query Data**: Use `/query` endpoint  
3. **Check Results**: Use `/info` endpoint

See [SUPPORTED_FILE_FORMATS.md](SUPPORTED_FILE_FORMATS.md) for detailed format information.

---

**Happy uploading!** 📄
