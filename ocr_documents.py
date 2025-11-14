#!/usr/bin/env python3
"""
OCR Processing for Image-Based Epstein Documents
Handles scanned PDFs and image files that require OCR
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import argparse

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("ERROR: OCR libraries not installed.")
    print("Install with: pip install -r requirements-ocr.txt")
    print("Also install system Tesseract: sudo apt-get install tesseract-ocr")
    sys.exit(1)

try:
    from pdf2image import convert_from_path
except ImportError:
    print("WARNING: pdf2image not installed. PDF processing will be limited.")
    print("Install with: pip install pdf2image")
    print("Also install poppler: sudo apt-get install poppler-utils")
    convert_from_path = None

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Note: Install tqdm for progress bars: pip install tqdm")


# Configuration
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "documents"


def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception as e:
        print(f"ERROR: Tesseract not found: {e}")
        print("\nInstall Tesseract OCR:")
        print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("  macOS: brew install tesseract")
        print("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        return False


def ocr_image_file(image_path, output_path):
    """
    OCR a single image file (JPG, PNG, TIFF, etc.)

    Args:
        image_path: Path to image file
        output_path: Path to save text output

    Returns:
        bool: True if successful
    """
    try:
        # Open image
        image = Image.open(image_path)

        # Perform OCR
        text = pytesseract.image_to_string(image, lang='eng')

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        return True

    except Exception as e:
        print(f"  Error OCR'ing {image_path.name}: {e}")
        return False


def ocr_pdf_file(pdf_path, output_path):
    """
    OCR a PDF file (handles scanned/image-based PDFs)

    Args:
        pdf_path: Path to PDF file
        output_path: Path to save text output

    Returns:
        bool: True if successful
    """
    if not convert_from_path:
        print(f"  pdf2image not available. Skipping {pdf_path.name}")
        return False

    try:
        # Convert PDF pages to images
        print(f"  Converting PDF to images: {pdf_path.name}")
        images = convert_from_path(str(pdf_path), dpi=300)

        # OCR each page
        all_text = []

        iterator = enumerate(images, 1)
        if HAS_TQDM and len(images) > 10:
            iterator = tqdm(iterator, total=len(images), desc="  OCR pages", leave=False)

        for page_num, image in iterator:
            try:
                text = pytesseract.image_to_string(image, lang='eng')
                all_text.append(f"\n--- Page {page_num} ---\n{text}")
            except Exception as e:
                print(f"    Error on page {page_num}: {e}")
                all_text.append(f"\n--- Page {page_num} ---\n[OCR ERROR]\n")

        # Save combined text
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))

        return True

    except Exception as e:
        print(f"  Error OCR'ing PDF {pdf_path.name}: {e}")
        return False


def process_directory(directory, file_types=None, force=False):
    """
    OCR all files in a directory

    Args:
        directory: Directory containing files to OCR
        file_types: List of file extensions to process (default: ['pdf', 'jpg', 'png', 'tiff'])
        force: Re-OCR files even if .txt already exists

    Returns:
        tuple: (success_count, error_count, skipped_count)
    """
    directory = Path(directory)

    if not directory.exists():
        print(f"ERROR: Directory not found: {directory}")
        return (0, 0, 0)

    if file_types is None:
        file_types = ['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif']

    # Find all matching files
    all_files = []
    for ext in file_types:
        all_files.extend(directory.glob(f"*.{ext}"))
        all_files.extend(directory.glob(f"*.{ext.upper()}"))

    if not all_files:
        print(f"No files found with extensions: {file_types}")
        return (0, 0, 0)

    print(f"\nFound {len(all_files)} files to process in {directory}")
    print("=" * 70)

    success = 0
    errors = 0
    skipped = 0

    # Create iterator with optional progress bar
    iterator = all_files
    if HAS_TQDM:
        iterator = tqdm(all_files, desc="Processing files")

    for file_path in iterator:
        # Determine output path
        txt_path = file_path.with_suffix('.txt')

        # Skip if already processed (unless force)
        if txt_path.exists() and not force:
            if not HAS_TQDM:
                print(f"⊘ Skipping (already processed): {file_path.name}")
            skipped += 1
            continue

        # Display progress
        if not HAS_TQDM:
            print(f"\nProcessing: {file_path.name}")

        # Process based on file type
        ext = file_path.suffix.lower()

        if ext == '.pdf':
            result = ocr_pdf_file(file_path, txt_path)
        else:
            result = ocr_image_file(file_path, txt_path)

        if result:
            success += 1
            if not HAS_TQDM:
                print(f"✓ OCR complete: {txt_path.name}")
        else:
            errors += 1

    return (success, errors, skipped)


def main():
    parser = argparse.ArgumentParser(
        description='OCR image-based Epstein documents (scanned PDFs and images)'
    )

    parser.add_argument(
        'directory',
        type=str,
        help='Directory containing files to OCR'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Re-OCR files even if .txt already exists'
    )

    parser.add_argument(
        '--types',
        type=str,
        nargs='+',
        default=['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'],
        help='File types to process (default: pdf jpg jpeg png tiff tif)'
    )

    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if Tesseract is installed and exit'
    )

    args = parser.parse_args()

    # Check for Tesseract
    if not check_tesseract():
        sys.exit(1)

    if args.check:
        print("✓ Tesseract is installed and working!")
        version = pytesseract.get_tesseract_version()
        print(f"  Version: {version}")
        sys.exit(0)

    # Process directory
    print("=" * 70)
    print("OCR DOCUMENT PROCESSOR")
    print("=" * 70)
    print(f"Directory: {args.directory}")
    print(f"File types: {', '.join(args.types)}")
    print(f"Force re-OCR: {args.force}")
    print()

    start_time = datetime.now()

    success, errors, skipped = process_directory(
        args.directory,
        file_types=args.types,
        force=args.force
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    # Summary
    print("\n" + "=" * 70)
    print("OCR PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Successful: {success}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    print(f"Total files: {success + errors + skipped}")
    print(f"Time elapsed: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print("=" * 70)

    if success > 0:
        print("\nNext steps:")
        print("1. Rebuild search index:")
        print("   python search_index.py --force")
        print("\n2. Start search API:")
        print("   python search_api.py")


if __name__ == '__main__':
    main()
