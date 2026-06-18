"""
Main entry point for testing the RAG system via CLI.
"""

import sys
import argparse
from pathlib import Path
from src.config import config
from src.utils.logger import get_logger
from src.rag.pipeline import RAGPipeline

logger = get_logger(__name__, config.log_level)


def ingest_command(args):
    """Handle ingest command"""
    pipeline = RAGPipeline()
    
    file_path = Path(args.file)
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return 1
    
    logger.info(f"Ingesting file: {file_path}")
    result = pipeline.ingest_document(str(file_path))
    
    if result["success"]:
        logger.info(f"✓ Success: {result['message']}")
        return 0
    else:
        logger.error(f"✗ Failed: {result.get('error', 'Unknown error')}")
        return 1


def query_command(args):
    """Handle query command"""
    pipeline = RAGPipeline()
    
    query = args.query
    logger.info(f"Processing query: {query}")
    
    result = pipeline.query(query, stream=args.stream)
    
    print("\n" + "="*80)
    print(f"Query: {result['query']}")
    print("="*80)
    print(f"Response:\n{result['response']}")
    print("="*80)
    
    if result['sources']:
        print(f"\nSources ({len(result['sources'])} found):")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source.get('source', 'Unknown')}")
    else:
        print("No sources found.")
    
    print("="*80 + "\n")
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Ollama RAG Enterprise Demo - CLI Interface"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a document")
    ingest_parser.add_argument("file", help="Path to file to ingest")
    ingest_parser.set_defaults(func=ingest_command)
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the system")
    query_parser.add_argument("query", help="Query string")
    query_parser.add_argument("--stream", action="store_true", help="Stream response")
    query_parser.set_defaults(func=query_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
