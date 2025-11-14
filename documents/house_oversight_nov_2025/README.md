# House Oversight Committee - November 2025 Release

**Description**: 20,000+ pages from Epstein estate
**Released**: November 12, 2025
**Source**: Estate of Jeffrey Epstein (via House Oversight Committee)
**Status**: ⏳ **Not yet downloaded**

## Direct Download Link

**Google Drive Folder**: https://drive.google.com/drive/folders/1Nc-qWHpGWrkUJ7_DO0o2-Ss_tVAfGasR

## How to Download

### Method 1: Direct Google Drive Download (Recommended)

1. **Visit the Google Drive link above**
2. **Download the entire folder**:
   - Click on the folder name
   - Click the three dots menu (⋮) or "Download" button
   - Select "Download" to get all files as ZIP
   - Or download individual files if preferred
3. **Extract downloaded files** (if ZIP archive)
4. **Move files to this directory**: `/documents/house_oversight_nov_2025/`
5. **Convert PDFs to text**:
   ```bash
   cd /path/to/EpsteinFiles
   python download_and_convert.py --convert documents/house_oversight_nov_2025/
   ```
6. **Rebuild search index**:
   ```bash
   python search_index.py --force
   ```

### Method 2: Automated Download (Advanced)

For programmatic download, you can use Google Drive CLI tools like `gdown` or `rclone`:

```bash
# Using gdown (install: pip install gdown)
# Note: May require authentication for large folders

# Or use the download script (requires direct file URLs)
python download_and_convert.py --download estate_nov_2025
```

**Note**: Google Drive folder links work best with browser download. For automation, consider using `rclone` with Google Drive integration.

## Contents

- **Emails**: Including Epstein to Michael Wolff (Jan 31, 2019) mentioning Trump
- **Financial documents**: Market reports, financial correspondence
- **Court documents**: Additional legal filings from Epstein cases
- **Correspondence**: Emails showing Epstein's displeasure with Trump presidency

## Key Findings

### Epstein Email to Michael Wolff (HOUSE_OVERSIGHT_030411)
Date: January 31, 2019

> "[she] worked at mara lago. . she was the one that accused prince andrew. . trump said he asked me to resign, never a member ever. . **of course he knew about the girls as he asked ghislaine to stop**"

This email contains Epstein's claim that Trump "knew about the girls" and asked Ghislaine Maxwell to "stop" recruiting at Mar-a-Lago.

## Notes

This release includes substantial new email correspondence not previously public. Democrats and Republicans on the House Oversight Committee both released portions of this tranche, with different emphases.
