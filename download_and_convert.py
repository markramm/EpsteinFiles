#!/usr/bin/env python3
"""
Epstein Files Document Downloader and Converter
Downloads public documents and converts PDFs to searchable text format
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
import argparse

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed. Install with: pip install PyPDF2")
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    print("pdfplumber not installed. Install with: pip install pdfplumber")
    pdfplumber = None


# Configuration
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "documents"

# Document sources - ADD DIRECT DOWNLOAD URLs HERE
DOCUMENT_SOURCES = {
    "doj_sep_2025": {
        "dir": DOCS_DIR / "doj_release_sep_2025",
        "description": "DOJ September 2025 Release (33,295 pages)",
        "dropbox_folder": "https://www.dropbox.com/scl/fo/98fthv8otekjk28lcrnc5/AIn3egnE58MYe4Bn4fliVBw?rlkey=m7p8e9omml96fgxl13kr2nuyt&e=1&dl=0",
        "urls": [
            # Note: Dropbox folder links require manual download via browser
            # For individual file URLs, add them here for automated download
            # Dropbox API or folder download tools would be needed for automation
        ]
    },
    "estate_nov_2025": {
        "dir": DOCS_DIR / "house_oversight_nov_2025",
        "description": "Epstein Estate November 2025 (20,000 pages)",
        "google_drive_folder": "https://drive.google.com/drive/folders/1Nc-qWHpGWrkUJ7_DO0o2-Ss_tVAfGasR",
        "urls": [
            # Note: Google Drive folder links require manual download via browser
            # For individual file URLs, add them here for automated download
            # Consider using gdown or rclone for automation
        ]
    },
    "court_docs": {
        "dir": DOCS_DIR / "court_documents",
        "description": "Court Documents",
        "urls": [
            # Add PACER or court archive links here
        ]
    }
}


def download_file(url, dest_path):
    """
    Download a file from URL to destination path

    Args:
        url: URL to download from
        dest_path: Local path to save file
    """
    print(f"Downloading: {url}")
    print(f"Saving to: {dest_path}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end='')

        print(f"\n✓ Downloaded: {dest_path.name}")
        return True

    except Exception as e:
        print(f"\n✗ Error downloading {url}: {e}")
        return False


def convert_pdf_to_text_pypdf2(pdf_path, txt_path):
    """Convert PDF to text using PyPDF2"""
    if not PyPDF2:
        return False

    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = []

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content.append(page.extract_text())

            full_text = '\n'.join(text_content)

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(full_text)

            return True

    except Exception as e:
        print(f"  PyPDF2 error: {e}")
        return False


def convert_pdf_to_text_pdfplumber(pdf_path, txt_path):
    """Convert PDF to text using pdfplumber (better OCR support)"""
    if not pdfplumber:
        return False

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []

            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_content.append(text)

            full_text = '\n'.join(text_content)

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(full_text)

            return True

    except Exception as e:
        print(f"  pdfplumber error: {e}")
        return False


def convert_pdf_to_text(pdf_path, txt_path):
    """
    Convert PDF to text, trying multiple methods

    Args:
        pdf_path: Path to PDF file
        txt_path: Path to output text file
    """
    print(f"Converting: {pdf_path.name}")

    # Try pdfplumber first (better quality)
    if convert_pdf_to_text_pdfplumber(pdf_path, txt_path):
        print(f"✓ Converted with pdfplumber: {txt_path.name}")
        return True

    # Fall back to PyPDF2
    if convert_pdf_to_text_pypdf2(pdf_path, txt_path):
        print(f"✓ Converted with PyPDF2: {txt_path.name}")
        return True

    # Try system pdftotext if available
    try:
        import subprocess
        result = subprocess.run(
            ['pdftotext', str(pdf_path), str(txt_path)],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"✓ Converted with pdftotext: {txt_path.name}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(f"✗ Failed to convert: {pdf_path.name}")
    return False


def convert_directory_pdfs(directory):
    """
    Convert all PDFs in a directory to text files

    Args:
        directory: Directory containing PDFs
    """
    directory = Path(directory)
    pdf_files = list(directory.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return

    print(f"\nFound {len(pdf_files)} PDF files in {directory}")
    converted = 0
    failed = 0

    for pdf_path in pdf_files:
        txt_path = pdf_path.with_suffix('.txt')

        # Skip if already converted
        if txt_path.exists():
            print(f"⊘ Skipping (already converted): {pdf_path.name}")
            continue

        if convert_pdf_to_text(pdf_path, txt_path):
            converted += 1
        else:
            failed += 1

    print(f"\nConversion complete:")
    print(f"  Converted: {converted}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(pdf_files)}")


def download_source(source_key):
    """Download all files for a specific source"""
    source = DOCUMENT_SOURCES.get(source_key)

    if not source:
        print(f"Unknown source: {source_key}")
        return

    print("=" * 70)
    print(f"DOWNLOADING: {source['description']}")
    print("=" * 70)

    # Create directory if it doesn't exist
    source['dir'].mkdir(parents=True, exist_ok=True)

    # Download all URLs
    if not source['urls']:
        print("No URLs configured for this source yet.")
        print("Please add download URLs to DOCUMENT_SOURCES in this script.")
        return

    downloaded = 0
    for url in source['urls']:
        # Extract filename from URL or use timestamp
        filename = url.split('/')[-1]
        if not filename or '?' in filename:
            filename = f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        dest_path = source['dir'] / filename

        if download_file(url, dest_path):
            downloaded += 1

    print(f"\nDownloaded {downloaded}/{len(source['urls'])} files")

    # Optionally convert PDFs immediately
    response = input("\nConvert PDFs to text now? (y/n): ")
    if response.lower() == 'y':
        convert_directory_pdfs(source['dir'])


def list_sources():
    """List all available document sources"""
    print("=" * 70)
    print("AVAILABLE DOCUMENT SOURCES")
    print("=" * 70)

    for key, source in DOCUMENT_SOURCES.items():
        print(f"\n{key}:")
        print(f"  Description: {source['description']}")
        print(f"  Directory: {source['dir']}")

        # Show Dropbox folder if available
        if 'dropbox_folder' in source:
            print(f"  Dropbox Folder: {source['dropbox_folder']}")
            print(f"  Note: Download manually via browser (Dropbox folder link)")

        # Show Google Drive folder if available
        if 'google_drive_folder' in source:
            print(f"  Google Drive Folder: {source['google_drive_folder']}")
            print(f"  Note: Download manually via browser (Google Drive folder link)")

        print(f"  URLs configured: {len(source['urls'])}")

        # Determine status
        if source['urls']:
            status = "Ready for automated download"
        elif 'dropbox_folder' in source:
            status = "Manual download available (Dropbox)"
        elif 'google_drive_folder' in source:
            status = "Manual download available (Google Drive)"
        else:
            status = "URLs not configured"

        print(f"  Status: {status}")


def main():
    parser = argparse.ArgumentParser(
        description='Download and convert Epstein documents to searchable text'
    )

    parser.add_argument(
        '--download',
        choices=list(DOCUMENT_SOURCES.keys()),
        help='Download documents from specified source'
    )

    parser.add_argument(
        '--convert',
        type=str,
        help='Convert PDFs in specified directory to text'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available sources'
    )

    args = parser.parse_args()

    if args.list:
        list_sources()

    elif args.download:
        download_source(args.download)

    elif args.convert:
        convert_directory_pdfs(args.convert)

    else:
        parser.print_help()
        print("\n" + "=" * 70)
        print("QUICK START GUIDE")
        print("=" * 70)
        print("\n1. List available sources:")
        print("   python download_and_convert.py --list")
        print("\n2. Download from a source:")
        print("   python download_and_convert.py --download doj_sep_2025")
        print("\n3. Convert PDFs in a directory:")
        print("   python download_and_convert.py --convert /path/to/pdfs")
        print("\nNote: You must first add download URLs to the DOCUMENT_SOURCES")
        print("dictionary in this script (lines 25-45)")


if __name__ == '__main__':
    main()
