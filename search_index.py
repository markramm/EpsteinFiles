#!/usr/bin/env python3
"""
Epstein Files Full-Text Search Index
Builds and maintains a Whoosh search index for the House Oversight documents
"""

import os
import sys
from pathlib import Path
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, DATETIME, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import And, Or, Term
from whoosh import scoring
from datetime import datetime
import re

# Configuration
EPSTEIN_FILES_DIR = Path(__file__).parent
INDEX_DIR = EPSTEIN_FILES_DIR / "search_index"

# Automatically discover all document directories
DOCUMENTS_DIRS = []
documents_root = EPSTEIN_FILES_DIR / "documents"
if documents_root.exists():
    # Find all subdirectories that contain .txt files
    for source_dir in documents_root.iterdir():
        if source_dir.is_dir() and source_dir.name != '__pycache__':
            # Check if this directory has .txt files
            if list(source_dir.glob("*.txt")):
                DOCUMENTS_DIRS.append(source_dir)
            # Also check subdirectories (e.g., 001, 002 folders)
            for subdir in source_dir.iterdir():
                if subdir.is_dir() and list(subdir.glob("*.txt")):
                    DOCUMENTS_DIRS.append(subdir)

# Fallback to old structure if documents/ doesn't exist yet
if not DOCUMENTS_DIRS:
    old_001 = EPSTEIN_FILES_DIR / "001"
    old_002 = EPSTEIN_FILES_DIR / "002"
    if old_001.exists():
        DOCUMENTS_DIRS.append(old_001)
    if old_002.exists():
        DOCUMENTS_DIRS.append(old_002)

# Schema definition
SCHEMA = Schema(
    filepath=ID(stored=True, unique=True),
    filename=ID(stored=True),
    doc_id=ID(stored=True),  # e.g., "HOUSE_OVERSIGHT_010477"
    content=TEXT(stored=True, field_boost=1.0),
    content_preview=TEXT(stored=True),  # First 500 chars for excerpts
    file_size=NUMERIC(stored=True),
    indexed_at=DATETIME(stored=True)
)


def extract_doc_id(filename):
    """Extract document ID from filename: HOUSE_OVERSIGHT_010477.txt -> HOUSE_OVERSIGHT_010477"""
    return Path(filename).stem


def clean_text(text):
    """Clean OCR artifacts and normalize text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove form feed characters
    text = text.replace('\f', ' ')
    # Remove BOM if present
    text = text.replace('\ufeff', '')
    return text.strip()


def index_documents(writer, force_reindex=False):
    """
    Index all documents from the epstein_files directories

    Args:
        writer: Whoosh IndexWriter instance
        force_reindex: If True, reindex all files even if already indexed
    """
    indexed_count = 0
    error_count = 0
    skipped_count = 0

    for docs_dir in DOCUMENTS_DIRS:
        if not docs_dir.exists():
            print(f"Warning: Directory not found: {docs_dir}")
            continue

        print(f"\nIndexing documents from: {docs_dir}")

        for txt_file in sorted(docs_dir.glob("*.txt")):
            try:
                # Check if already indexed (unless force reindex)
                if not force_reindex:
                    # This is a simple check - in production you'd check modification time
                    pass

                # Read file content
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Try with latin-1 encoding as fallback
                    with open(txt_file, 'r', encoding='latin-1') as f:
                        content = f.read()

                # Clean the content
                content = clean_text(content)

                if not content or len(content) < 10:
                    print(f"  Skipping empty/tiny file: {txt_file.name}")
                    skipped_count += 1
                    continue

                # Extract document ID
                doc_id = extract_doc_id(txt_file.name)

                # Create preview (first 500 chars)
                preview = content[:500] if len(content) > 500 else content

                # Add to index
                writer.add_document(
                    filepath=str(txt_file.absolute()),
                    filename=txt_file.name,
                    doc_id=doc_id,
                    content=content,
                    content_preview=preview,
                    file_size=txt_file.stat().st_size,
                    indexed_at=datetime.now()
                )

                indexed_count += 1

                if indexed_count % 100 == 0:
                    print(f"  Indexed {indexed_count} documents...")

            except Exception as e:
                print(f"  Error indexing {txt_file.name}: {e}")
                error_count += 1

    return indexed_count, error_count, skipped_count


def build_index(force=False):
    """
    Build or rebuild the search index

    Args:
        force: If True, delete existing index and rebuild from scratch
    """
    print("=" * 70)
    print("EPSTEIN FILES SEARCH INDEX BUILDER")
    print("=" * 70)

    # Create index directory if it doesn't exist
    INDEX_DIR.mkdir(exist_ok=True)

    # Check if index exists
    index_exists = exists_in(str(INDEX_DIR))

    if index_exists and not force:
        print(f"\nIndex already exists at: {INDEX_DIR}")
        print("Use --force to rebuild from scratch")
        response = input("Update existing index? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
        ix = open_dir(str(INDEX_DIR))
    else:
        if index_exists and force:
            print(f"\nForce rebuild: Deleting existing index...")
            import shutil
            shutil.rmtree(INDEX_DIR)
            INDEX_DIR.mkdir(exist_ok=True)

        print(f"\nCreating new index at: {INDEX_DIR}")
        ix = create_in(str(INDEX_DIR), SCHEMA)

    # Index documents
    print("\nStarting indexing process...")
    start_time = datetime.now()

    writer = ix.writer()
    try:
        indexed, errors, skipped = index_documents(writer, force_reindex=force)
        writer.commit()

        elapsed = (datetime.now() - start_time).total_seconds()

        print("\n" + "=" * 70)
        print("INDEXING COMPLETE")
        print("=" * 70)
        print(f"Documents indexed: {indexed}")
        print(f"Documents skipped: {skipped}")
        print(f"Errors: {errors}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print(f"Index location: {INDEX_DIR}")
        print("=" * 70)

    except Exception as e:
        print(f"\nFatal error during indexing: {e}")
        writer.cancel()
        raise


def test_search(query_string, limit=5):
    """
    Test the search index with a query

    Args:
        query_string: Search query
        limit: Maximum number of results to return
    """
    if not exists_in(str(INDEX_DIR)):
        print("Error: Index not found. Run build_index() first.")
        return

    ix = open_dir(str(INDEX_DIR))

    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        # Search in content field
        parser = QueryParser("content", ix.schema)
        query = parser.parse(query_string)

        results = searcher.search(query, limit=limit)

        print(f"\nSearch results for: '{query_string}'")
        print(f"Found {len(results)} results (showing top {limit})")
        print("=" * 70)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. Document: {result['doc_id']}")
            print(f"   File: {result['filename']}")
            print(f"   Score: {result.score:.2f}")

            # Show excerpt with highlighting
            preview = result['content_preview']
            if len(preview) > 200:
                preview = preview[:200] + "..."
            print(f"   Preview: {preview}")
            print("-" * 70)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Build search index for Epstein files')
    parser.add_argument('--force', action='store_true', help='Force rebuild of index')
    parser.add_argument('--test', type=str, help='Test search with query')

    args = parser.parse_args()

    if args.test:
        test_search(args.test)
    else:
        build_index(force=args.force)
