# House Oversight Committee - Earlier Estate Documents (September 2025)

**Description**: Additional tranche from Epstein estate
**Released**: September 8-9, 2025
**Source**: Estate of Jeffrey Epstein (via House Oversight Committee)
**Status**: ⏳ **Not yet downloaded**

## Direct Download Link

**Dropbox Folder**: https://www.dropbox.com/scl/fo/azl4abiwwixtvezmz0617/ANVZACgh4aPQ-TcxCKi0FDw?rlkey=aqg68si6y246f2b15kro9zmqh&e=2&st=7nh3wzuq&dl=0

## How to Download

### Method 1: Direct Dropbox Download (Recommended)

1. **Visit the Dropbox link above**
2. **Download the entire folder**:
   - Click "Download" button (top right)
   - Select "Download Folder"
   - Or download individual files if needed
3. **Extract downloaded files** (if ZIP archive)
4. **Move files to this directory**: `/documents/estate_sep_2025/`
5. **Convert PDFs to text**:
   ```bash
   cd /path/to/EpsteinFiles
   python download_and_convert.py --convert documents/estate_sep_2025/
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
python download_and_convert.py --download estate_sep_2025
```

**Note**: Dropbox shared folder links are designed for browser access. For bulk downloads, manual download via browser is often most reliable.

## Contents

- **"Birthday book"**: Contact list or address book
- **Emails**: Additional estate correspondence
- **Financial documents**: Estate-related records
- **Other correspondence**: Various documents from estate

## Notes

This is an earlier release of estate documents, separate from the larger November 2025 estate release. Released shortly after the DOJ September 2025 release.

## Official Source

**House Oversight Page**: https://oversight.house.gov/release/oversight-committee-releases-records-provided-by-the-epstein-estate-chairman-comer-provides-statement/
