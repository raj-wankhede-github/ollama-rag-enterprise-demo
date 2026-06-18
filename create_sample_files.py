#!/usr/bin/env python
"""
Test script for demonstrating multi-format file ingestion.
Creates sample files and tests the ingestion process.
"""

import os
import csv
import tempfile
import json
from pathlib import Path

def create_sample_csv():
    """Create a sample CSV file"""
    csv_path = Path("sample_data.csv")
    
    data = [
        ["Employee", "Department", "Salary", "Years"],
        ["Alice Johnson", "Engineering", "120000", "5"],
        ["Bob Smith", "Marketing", "95000", "3"],
        ["Charlie Brown", "Sales", "85000", "4"],
        ["Diana Prince", "HR", "90000", "2"],
        ["Eve Davis", "Engineering", "130000", "7"],
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"✓ Created sample CSV: {csv_path}")
    print(f"  - 5 employees across multiple departments")
    print(f"  - Total size: {csv_path.stat().st_size} bytes")
    return csv_path


def create_sample_xlsx():
    """Create a sample XLSX file"""
    try:
        from openpyxl import Workbook
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Sales"
        
        # Add headers
        headers = ["Date", "Product", "Amount", "Region"]
        ws.append(headers)
        
        # Add data rows
        data = [
            ["2024-01-01", "Widget A", 1000, "North"],
            ["2024-01-02", "Widget B", 1500, "South"],
            ["2024-01-03", "Widget A", 2000, "East"],
            ["2024-01-04", "Widget C", 1200, "West"],
            ["2024-01-05", "Widget B", 1800, "North"],
        ]
        
        for row in data:
            ws.append(row)
        
        # Create second sheet
        ws2 = wb.create_sheet("Inventory")
        ws2.append(["Product", "Stock", "Reorder Level"])
        ws2.append(["Widget A", 500, 100])
        ws2.append(["Widget B", 300, 50])
        ws2.append(["Widget C", 200, 75])
        
        xlsx_path = Path("sample_sales.xlsx")
        wb.save(xlsx_path)
        
        print(f"✓ Created sample XLSX: {xlsx_path}")
        print(f"  - 2 sheets: Sales and Inventory")
        print(f"  - 5 sales records + 3 inventory items")
        print(f"  - Total size: {xlsx_path.stat().st_size} bytes")
        return xlsx_path
    except ImportError:
        print("✗ openpyxl not installed, skipping XLSX creation")
        return None


def create_sample_xls():
    """Create a sample XLS file using openpyxl (saves as XLSX, can be opened in Excel)"""
    # Note: Python doesn't have good support for creating actual .xls files
    # This demonstrates how to create an Excel file
    print("✓ Note: XLS support is for reading legacy Excel files")
    print("  - To test, use an existing .xls file or create in Excel 97-2003 format")
    return None


def create_sample_txt():
    """Create a sample TXT file"""
    txt_path = Path("sample_document.txt")
    
    content = """Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that focuses on the development 
of computer programs that can learn and improve from experience without being explicitly programmed.

Key Concepts:

1. Supervised Learning
   - Classification: Predicting categories
   - Regression: Predicting continuous values
   - Examples: Email spam detection, house price prediction

2. Unsupervised Learning
   - Clustering: Grouping similar data points
   - Dimensionality Reduction: Reducing data complexity
   - Examples: Customer segmentation, anomaly detection

3. Reinforcement Learning
   - Agent learns by interacting with environment
   - Rewards and penalties guide learning
   - Examples: Game playing, robotics, autonomous driving

Applications:
- Healthcare: Disease diagnosis, drug discovery
- Finance: Fraud detection, market analysis
- Retail: Product recommendations, demand forecasting
- Manufacturing: Quality control, predictive maintenance
"""
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created sample TXT: {txt_path}")
    print(f"  - Machine Learning introduction")
    print(f"  - Total size: {txt_path.stat().st_size} bytes")
    return txt_path


def create_sample_markdown():
    """Create a sample Markdown file"""
    md_path = Path("sample_guide.md")
    
    content = """# Getting Started with RAG Systems

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
   curl -X POST "http://localhost:8000/query" \\
     -H "Content-Type: application/json" \\
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
"""
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created sample MD: {md_path}")
    print(f"  - RAG system guide with markdown formatting")
    print(f"  - Total size: {md_path.stat().st_size} bytes")
    return md_path


def create_sample_files():
    """Create all sample files for testing"""
    print("=" * 60)
    print("Creating Sample Files for Testing")
    print("=" * 60)
    print()
    
    files = {
        "CSV": create_sample_csv(),
        "XLSX": create_sample_xlsx(),
        "XLS": create_sample_xls(),
        "TXT": create_sample_txt(),
        "MD": create_sample_markdown(),
    }
    
    print()
    print("=" * 60)
    print("Sample Files Created")
    print("=" * 60)
    print()
    
    print("Files ready for upload:")
    for fmt, path in files.items():
        if path:
            print(f"  ✓ {fmt:6s}: {path}")
    
    print()
    print("Next steps:")
    print("1. Start the server: python main.py")
    print("2. Upload files:")
    print()
    for fmt, path in files.items():
        if path:
            print(f"   curl -X POST 'http://localhost:8000/ingest' \\")
            print(f"     -F 'file=@{path}'")
            print()
    
    print("3. Query the system:")
    print()
    print("   curl -X POST 'http://localhost:8000/query' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"query\": \"Your question here\"}'")
    print()
    
    return files


def test_document_processor():
    """Test the document processor with sample files"""
    from src.rag.document_processor import DocumentProcessor
    
    print("=" * 60)
    print("Testing Document Processor")
    print("=" * 60)
    print()
    
    processor = DocumentProcessor()
    
    # Create test files
    files = create_sample_files()
    
    print("Processing files...")
    print()
    
    for fmt, filepath in files.items():
        if not filepath:
            continue
        
        print(f"Processing {fmt} file: {filepath}")
        try:
            # Process the file
            documents = processor.process_file(str(filepath))
            
            if documents:
                print(f"  ✓ Successfully processed into {len(documents)} chunks")
                print(f"  - First chunk length: {len(documents[0]['content'])} chars")
                print(f"  - File type: {documents[0]['metadata'].get('file_type', 'unknown')}")
                print(f"  - Sample content: {documents[0]['content'][:100]}...")
            else:
                print(f"  ✗ Failed to process file")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run full test
        try:
            test_document_processor()
        except Exception as e:
            print(f"Error during testing: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Just create sample files
        create_sample_files()


if __name__ == "__main__":
    main()
