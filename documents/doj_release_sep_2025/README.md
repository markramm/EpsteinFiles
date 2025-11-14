# Department of Justice - September 2025 Release

**Description**: 33,295 pages of DOJ Epstein records
**Released**: September 2, 2025
**Source**: U.S. Department of Justice (via House Oversight Committee subpoena)
**Status**: ⏳ **Not yet downloaded**

## How to Download

1. Visit: https://oversight.house.gov/release/oversight-committee-releases-epstein-records-provided-by-the-department-of-justice/
2. Look for Google Drive or Dropbox download links on the page
3. Download all PDF/document files
4. Save to this directory: `/documents/doj_release_sep_2025/`
5. Convert PDFs to text:
   ```bash
   cd /path/to/EpsteinFiles
   python download_and_convert.py --convert documents/doj_release_sep_2025/
   ```
6. Rebuild search index:
   ```bash
   python search_index.py --force
   ```

## Contents

- Court documents
- Flight logs
- Prison communications
- Previously public court filings (~97% of content)
- New flight location data (~3% of content, under 1,000 pages)

## Notes

Per House Democrats' analysis, approximately 97% of these documents were already in the public domain prior to this release. The new information consists primarily of flight location data for Epstein's aircraft.
