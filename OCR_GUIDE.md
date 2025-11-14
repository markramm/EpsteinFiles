# OCR Guide for Image-Based Documents

**Important**: Many of the Epstein document releases are **scanned images** (image-based PDFs or JPG/PNG files) rather than text-based PDFs. These require **OCR (Optical Character Recognition)** to extract searchable text.

---

## Quick Start for OCR

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**
- Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases/

### 2. Install Python Dependencies

```bash
pip install -r requirements-ocr.txt
```

This installs:
- `pytesseract` - Python wrapper for Tesseract OCR
- `pdf2image` - Converts PDF pages to images
- `Pillow` - Image processing library
- `tqdm` - Progress bars

### 3. Check Installation

```bash
python ocr_documents.py --check
```

Should output:
```
✓ Tesseract is installed and working!
  Version: 5.x.x
```

### 4. Process Documents

```bash
# OCR a single directory
python ocr_documents.py documents/doj_release_sep_2025/

# Force re-process (overwrite existing .txt files)
python ocr_documents.py documents/doj_release_sep_2025/ --force

# Process specific file types only
python ocr_documents.py documents/court_documents/ --types pdf jpg png
```

### 5. Rebuild Search Index

```bash
python search_index.py --force
```

---

## Understanding the OCR Workflow

### Text-Based PDFs vs Image-Based Documents

**Text-Based PDFs** (fast):
- Already contain searchable text
- Extract with `pdftotext` or `PyPDF2`
- Processing time: Seconds per document

**Image-Based Documents** (slow):
- Scanned pages or photographs
- Require OCR to extract text
- Processing time: **Minutes per document**

### How to Identify Image Documents

```bash
# Try to extract text from a PDF
pdftotext sample.pdf -

# If output is empty or gibberish → image-based, needs OCR
# If output is readable text → text-based, no OCR needed
```

---

## Performance Expectations

### OCR Processing Speed

| Document Type | Pages | OCR Time (estimate) |
|--------------|-------|---------------------|
| Single page PDF | 1 | ~5-10 seconds |
| 10-page PDF | 10 | ~1-2 minutes |
| 100-page PDF | 100 | ~10-20 minutes |
| **DOJ Release (33,295 pages)** | 33,295 | **~28-55 hours** |
| **Estate Nov 2025 (20,000 pages)** | 20,000 | **~17-33 hours** |
| **All sources (60,000 pages)** | 60,000 | **~50-100 hours** |

**Note**: Times assume:
- Modern CPU (4+ cores)
- 300 DPI image quality
- English language OCR
- Sequential processing (not parallel)

### Optimization Tips

**1. Parallel Processing** (advanced):
```bash
# Process multiple files simultaneously
# Split documents into batches and run multiple OCR processes
```

**2. Lower DPI** (faster but less accurate):
```python
# In ocr_documents.py, line ~100:
# Change: images = convert_from_path(str(pdf_path), dpi=300)
# To:     images = convert_from_path(str(pdf_path), dpi=200)
```

**3. Process Selectively**:
```bash
# Only process PDFs you need to search
# Skip redundant or duplicate documents
```

---

## Workflow for Large Document Sets

### Recommended Approach

```bash
# 1. Download documents to appropriate directories
# (Via Dropbox/Google Drive links - manual download)

# 2. Extract ZIP files
cd downloads/
unzip "DOJ Epstein Files - First Production.zip"
mv "DOJ Epstein Files - First Production"/* /path/to/EpsteinFiles/documents/doj_release_sep_2025/

# 3. Check if OCR is needed
cd /path/to/EpsteinFiles
pdftotext documents/doj_release_sep_2025/sample.pdf -
# If empty/gibberish → proceed with OCR

# 4. Start OCR processing (this will take HOURS)
python ocr_documents.py documents/doj_release_sep_2025/

# Monitor progress with tqdm progress bars
# Can safely CTRL+C and resume later (skips already-processed files)

# 5. Rebuild search index after OCR completes
python search_index.py --force

# 6. Start search API
python search_api.py
```

### Running OCR in Background

```bash
# Run OCR in background (Linux/macOS)
nohup python ocr_documents.py documents/doj_release_sep_2025/ > ocr.log 2>&1 &

# Check progress
tail -f ocr.log

# Or use screen/tmux for persistent sessions
screen -S ocr
python ocr_documents.py documents/doj_release_sep_2025/
# CTRL+A then D to detach
# screen -r ocr to reattach
```

### Incremental Processing

```bash
# Process one directory at a time
python ocr_documents.py documents/doj_release_sep_2025/
# Wait for completion (~30 hours)

python ocr_documents.py documents/house_oversight_nov_2025/
# Wait for completion (~20 hours)

python ocr_documents.py documents/estate_sep_2025/
# Wait for completion (~5 hours)

python ocr_documents.py documents/court_documents/
# Wait for completion (~5 hours)

# Total: ~60 hours spread across days/weeks
```

---

## Troubleshooting

### "Tesseract not found"

**Problem**: System Tesseract not installed

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Verify installation
tesseract --version
```

### "pdf2image not found" or "poppler not found"

**Problem**: Poppler utilities not installed

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Verify installation
pdfinfo --version
```

### OCR Quality Issues

**Problem**: OCR produces garbage text or misses words

**Possible causes**:
- Low image quality
- Skewed/rotated pages
- Poor scan quality
- Non-English text

**Solutions**:
1. Increase DPI (300 → 600 in ocr_documents.py)
2. Pre-process images (deskew, contrast adjustment)
3. Try different OCR engines (compare Tesseract vs cloud OCR services)

### Out of Memory

**Problem**: System runs out of RAM during OCR

**Solution**:
```bash
# Process smaller batches
# Split large PDFs into smaller chunks
# Reduce DPI setting
# Close other applications
```

### Very Slow Processing

**Expected**: OCR is inherently slow for large document sets

**Optimizations**:
- Use faster CPU
- Process in parallel (multiple terminals/processes)
- Use cloud OCR services (Google Cloud Vision, AWS Textract) for faster processing
- Consider overnight/weekend processing

---

## Alternative: Cloud OCR Services

If local OCR is too slow, consider cloud services:

### Google Cloud Vision API
- Faster than local Tesseract
- Higher accuracy
- Costs: ~$1.50 per 1,000 pages
- For 60,000 pages: ~$90

### AWS Textract
- Similar speed/accuracy to Google
- Costs: ~$1.50 per 1,000 pages
- Better for tables/forms

### Azure Cognitive Services
- Comparable pricing and performance

**Note**: Cloud services require API keys and have privacy implications (uploading documents to cloud).

---

## Quality Verification

After OCR, verify quality:

```bash
# Check a sample .txt file
less documents/doj_release_sep_2025/SAMPLE_FILE.txt

# Look for:
# - Readable text (not gibberish)
# - Proper word spacing
# - Minimal OCR errors
# - Complete pages

# If quality is poor, consider:
# - Increasing DPI
# - Using cloud OCR
# - Manual review of critical documents
```

---

## Next Steps After OCR

1. **Rebuild search index** with OCR'd text:
   ```bash
   python search_index.py --force
   ```

2. **Test searches** to verify quality:
   ```bash
   python search_api.py
   # Visit http://127.0.0.1:5002/
   # Try searching for known terms
   ```

3. **Verify document counts**:
   ```bash
   # Count .txt files
   find documents/ -name "*.txt" | wc -l
   ```

4. **Check index statistics**:
   ```bash
   curl http://127.0.0.1:5002/api/epstein/stats
   ```

---

## Realistic Timeline

For a complete OCR processing of all Epstein documents:

**Conservative Estimate** (60,000 pages):
- OCR Processing: 50-100 hours (2-4 days continuous)
- Index Building: 30-60 minutes
- **Total**: ~3-5 days of processing time

**Recommended Approach**:
- Week 1: Download all documents
- Week 2-3: OCR DOJ release (largest, ~30 hours)
- Week 4: OCR estate documents (~25 hours)
- Week 5: OCR court documents (~5 hours)
- Week 6: Final index build and testing

**Or**: Use cloud OCR for 1-2 days total processing time (~$90 cost)

---

## Summary

- **Image-based documents require OCR** (most government releases)
- **OCR is slow but necessary** for searchability
- **Install Tesseract + pdf2image** for local processing
- **Expect 50-100 hours** for full 60,000 page corpus
- **Process incrementally** or use cloud services for speed
- **Verify quality** before relying on results

Good luck with your transparency project!
