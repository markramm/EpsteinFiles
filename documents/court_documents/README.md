# Court Documents - Various Unsealing Events

**Description**: Unsealed court filings, depositions, and legal documents
**Sources**: Federal courts via PACER and public archives
**Status**: ⏳ **Not yet downloaded**

## Major Court Document Releases

### 1. Giuffre v. Maxwell (January 2024)
**Case**: 1:15-cv-07433 (S.D.N.Y.)
**Judge**: Loretta Preska
**Unsealed**: January 4, 2024
**Content**:
- Depositions of key witnesses
- Exhibits and correspondence
- Flight logs and travel records
- Names of associates and acquaintances

**How to Access**:
- PACER: https://pacer.uscourts.gov/ (paid, $0.10/page)
- Court Listener: https://www.courtlistener.com/ (free archive)
- Archive.org: May have free copies of unsealed documents

### 2. DOJ Declassification (February 2025)
**Released by**: Attorney General Pamela Bondi
**Content**:
- FBI investigative files
- Heavily redacted
- Mostly previously reported information

**Status**: These may overlap with House Oversight releases

### 3. Other Relevant Cases
- **U.S. v. Epstein** (S.D. Fla. 2008) - Original plea deal case
- **U.S. v. Epstein** (S.D.N.Y. 2019) - Federal indictment (before death)
- **U.S. v. Maxwell** (S.D.N.Y. 2021) - Ghislaine Maxwell criminal trial

## How to Download

### Option 1: PACER (Official, Paid)
1. Create account: https://pacer.uscourts.gov/
2. Costs $0.10 per page
3. Free if quarterly charges < $30
4. Search for case number: 1:15-cv-07433
5. Download docket entries and documents
6. Save PDFs to this directory

### Option 2: Court Listener (Free Archive)
1. Visit: https://www.courtlistener.com/
2. Search: "Giuffre Maxwell" or "Jeffrey Epstein"
3. Browse available documents
4. Download PDFs (free)
5. Save to this directory

### Option 3: Archive.org
1. Search Archive.org for "Epstein court documents"
2. Look for collections of unsealed documents
3. Download available archives

### Option 4: News Organization Archives
Some news organizations archived and republished unsealed documents:
- Miami Herald Epstein coverage
- New York Times document databases
- ProPublica archives

## Processing Downloaded Documents

Once you have PDF files:

```bash
cd /path/to/EpsteinFiles

# Convert PDFs to text
python download_and_convert.py --convert documents/court_documents/

# Rebuild search index
python search_index.py --force
```

## Important Notes

### Grand Jury Transcripts - DENIED
Federal judges have **denied** requests to unseal Epstein grand jury transcripts:
- Florida grand jury (July 2025) - Denied
- New York grand jury (August 2025) - Denied

These remain sealed and are **not** part of this collection.

### Redactions
Court documents contain redactions for:
- Victim identities (by law)
- Ongoing investigations
- Privacy considerations

**Do not** attempt to remove or circumvent redactions. This is illegal.

## Legal & Ethical Considerations

✅ **DO**:
- Download officially unsealed documents
- Respect court-ordered redactions
- Cite documents properly
- Protect victim identities

❌ **DON'T**:
- Download sealed documents
- Remove redactions
- Spread victim identifying information
- Violate court orders

## Estimated Content

When downloaded, expect:
- 1,000-5,000 pages of court documents
- Depositions, motions, exhibits
- Previously public flight logs
- Correspondence entered as evidence

## Timeline of Unsealing

- **2024**: Major unsealing of Giuffre v. Maxwell documents
- **2025 Feb**: DOJ declassification (heavily redacted)
- **2025 Sep-Nov**: House Oversight releases (includes some court docs)
- **Ongoing**: Additional documents may be unsealed

Check news for updates on additional unsealing events.
