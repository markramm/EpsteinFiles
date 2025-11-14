# Department of Justice - September 2025 Release

**Description**: 33,295 pages of DOJ Epstein records
**Released**: September 2, 2025
**Source**: U.S. Department of Justice (via House Oversight Committee subpoena)
**Status**: ⏳ **Not yet downloaded**

## Direct Download Link

**Dropbox Folder**: https://www.dropbox.com/scl/fo/98fthv8otekjk28lcrnc5/AIn3egnE58MYe4Bn4fliVBw?rlkey=m7p8e9omml96fgxl13kr2nuyt&e=1&dl=0

## How to Download

### Method 1: Direct Dropbox Download (Recommended)

1. **Visit the Dropbox link above** (DOJ Epstein Files - First Production)
2. **Download the entire folder**:
   - Click "Download" button (top right)
   - Select "Download Folder"
   - Or download individual files if needed
3. **Extract downloaded files** (if ZIP archive)
4. **Move files to this directory**: `/documents/doj_release_sep_2025/`
5. **Convert PDFs to text**:
   ```bash
   cd /path/to/EpsteinFiles
   python download_and_convert.py --convert documents/doj_release_sep_2025/
   ```
6. **Rebuild search index**:
   ```bash
   python search_index.py --force
   ```

### Method 2: Automated Download (Advanced)

For programmatic download, you can use the Dropbox API or command-line tools:

```bash
# Using wget (if Dropbox provides direct links to files)
# Note: Dropbox folder links require special handling

# Or use the download script (requires Dropbox direct file URLs)
python download_and_convert.py --download doj_sep_2025
```

**Note**: Dropbox shared folder links are designed for browser access. For bulk downloads, manual download via browser is often most reliable.

## Contents

- Court documents
- Flight logs
- Prison communications
- Previously public court filings (~97% of content)
- New flight location data (~3% of content, under 1,000 pages)

## Notes

Per House Democrats' analysis, approximately 97% of these documents were already in the public domain prior to this release. The new information consists primarily of flight location data for Epstein's aircraft.
