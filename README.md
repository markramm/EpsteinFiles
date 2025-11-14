# Epstein Files Search Tool

**Full-text search engine for the 2,895 House Oversight Committee Epstein documents**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)

This open-source tool provides fast, full-text search capabilities for the Jeffrey Epstein documents released by the House Oversight Committee. It uses the Whoosh search library to enable researchers, journalists, and the public to quickly find relevant information across thousands of documents.

---

## 🎯 Purpose

The House Oversight Committee has released 2,895 documents related to Jeffrey Epstein, but searching through them manually is time-consuming and difficult. This tool:

- **Indexes all 2,895 documents** for instant full-text search
- **Provides a web interface** for easy searching
- **Offers a RESTful API** for programmatic access
- **Enables reproducible research** - others can verify findings

This tool was used to conduct the offshore financial infrastructure research documented in the [Master Integrated Report](analysis/MASTER_INTEGRATED_REPORT_PHASES_1_2_3.md).

---

## ✨ Features

- **Fast full-text search** across all 2,895 documents (sub-second queries)
- **Web interface** with highlighting and document preview
- **RESTful API** for programmatic access
- **Advanced query syntax** (AND, OR, NOT, phrase matching, wildcards)
- **Search in multiple fields** (content, document ID, filename)
- **BM25F ranking** for relevance scoring
- **Highlighted excerpts** showing search terms in context
- **Full document retrieval** for detailed analysis

---

## 📋 Requirements

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **2-3 GB disk space** (for documents and search index)

---

## 🚀 Quick Start

### 1. Clone or Download

```bash
# Clone repository (if on GitHub)
git clone https://github.com/YOUR_USERNAME/epstein-files-search.git
cd epstein-files-search

# Or download and extract ZIP
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install whoosh flask
```

### 3. Build Search Index

```bash
# Build the search index (takes 2-5 minutes for 2,895 documents)
python search_index.py --force
```

**Expected output:**
```
======================================================================
EPSTEIN FILES SEARCH INDEX BUILDER
======================================================================
Creating new index at: /path/to/search_index
Starting indexing process...
Indexed 100 documents...
Indexed 200 documents...
...
======================================================================
INDEXING COMPLETE
======================================================================
Documents indexed: 2895
Documents skipped: 0
Errors: 0
Time elapsed: 127.34 seconds
======================================================================
```

### 4. Start the Search Server

```bash
# Start the web server
python search_api.py
```

**Expected output:**
```
======================================================================
EPSTEIN FILES SEARCH API & WEB INTERFACE
======================================================================
Index location: /path/to/search_index
Index exists: True

Web Interface:
  http://127.0.0.1:5002/

API Endpoints:
  GET    /                           - Web search interface
  POST   /api/epstein/search        - Search documents
  GET    /api/epstein/document/<id> - Get full document
  GET    /api/epstein/stats         - Index statistics
======================================================================
```

### 5. Open Web Interface

Open your browser to: **http://127.0.0.1:5002/**

You'll see a web interface where you can:
- Enter search queries
- View highlighted results
- Read full documents
- Export findings

---

## 🔍 Search Examples

### Web Interface Examples

**Simple keyword search:**
```
Trump
```

**Phrase search (exact match):**
```
"Peter Thiel"
```

**Boolean operators:**
```
Trump AND Epstein
Russian OR Russia
NOT "public records"
```

**Multiple terms (any match):**
```
Thiel Bannon Kushner
```

**Complex queries:**
```
(Trump OR Clinton) AND "wire transfer"
"Mar-a-Lago" NOT public
```

### API Examples

**Python:**
```python
import requests

# Search query
response = requests.post('http://127.0.0.1:5002/api/epstein/search', json={
    'query': 'Trump AND Epstein',
    'limit': 20
})

results = response.json()
print(f"Found {results['total']} results")

for result in results['results']:
    print(f"Document: {result['doc_id']}")
    print(f"Excerpt: {result['excerpt'][:200]}...")
    print()
```

**cURL:**
```bash
# POST request
curl -X POST http://127.0.0.1:5002/api/epstein/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Peter Thiel", "limit": 10}'

# GET request
curl "http://127.0.0.1:5002/api/epstein/search?query=Thiel&limit=10"
```

**JavaScript:**
```javascript
fetch('http://127.0.0.1:5002/api/epstein/search', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'Trump', limit: 20})
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📚 API Documentation

### POST /api/epstein/search

Search documents with full-text query.

**Request:**
```json
{
  "query": "search terms",
  "limit": 20,
  "offset": 0,
  "highlight": true
}
```

**Response:**
```json
{
  "query": "search terms",
  "results": [
    {
      "doc_id": "HOUSE_OVERSIGHT_010477",
      "filename": "HOUSE_OVERSIGHT_010477.txt",
      "filepath": "/path/to/file.txt",
      "excerpt": "...highlighted excerpt...",
      "score": 12.34,
      "file_size": 45678
    }
  ],
  "total": 127,
  "offset": 0,
  "limit": 20,
  "has_more": true
}
```

### GET /api/epstein/document/<doc_id>

Retrieve full document content by ID.

**Response:**
```json
{
  "doc_id": "HOUSE_OVERSIGHT_010477",
  "filename": "HOUSE_OVERSIGHT_010477.txt",
  "filepath": "/path/to/file.txt",
  "content": "full document text...",
  "file_size": 45678,
  "indexed_at": "2025-11-14T12:34:56"
}
```

### GET /api/epstein/stats

Get index statistics.

**Response:**
```json
{
  "total_documents": 2895,
  "index_path": "/path/to/search_index"
}
```

### GET /api/epstein/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "index_initialized": true
}
```

---

## 🔬 Research Findings

This tool was used to conduct comprehensive research documented in:

- **[Master Integrated Report](analysis/MASTER_INTEGRATED_REPORT_PHASES_1_2_3.md)** - 33,000-word comprehensive analysis
- **[Phase 1: Intelligence Networks](analysis/PHASE_1_2_INTEGRATED_REPORT.md)** - Mossad, CIA, Russian connections
- **[Phase 2: Financial Infrastructure](analysis/phase2_financial/)** - 46+ offshore entities discovered
- **[Phase 3: Political Capture](analysis/phase3_political_capture.json)** - 12 compromised officials analyzed

### Key Search Queries Used in Research

**Officials mentioned:**
```
"Donald Trump" → 2,039 mentions
"Bill Clinton" → 939 mentions
"Bill Gates" → 666 mentions
"Prince Andrew" → 397 mentions
```

**Related terms:**
```
"Trump Tower" → 2,012 mentions
"Mar-a-Lago" → 302 mentions
"Lolita Express" → 157 mentions
"non-prosecution" → 469 mentions
```

**Cross-referencing:**
```
Trump AND "wire transfer"
Clinton AND "flight log"
Gates AND "foundation"
```

---

## 📁 Directory Structure

```
epstein_files/
├── README.md                  # This file
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
├── search_index.py           # Index builder
├── search_api.py             # Flask API & web interface
├── documents/                # Epstein files (2,895 .txt files)
│   └── house_oversight/
│       ├── 001/
│       └── 002/
├── search_index/             # Whoosh search index (generated)
└── analysis/                 # Research findings
    ├── MASTER_INTEGRATED_REPORT_PHASES_1_2_3.md
    ├── phase1_intelligence/
    ├── phase2_financial/
    └── phase3_political_capture.json
```

---

## 🛠️ Advanced Usage

### Rebuild Index

If documents are updated or index becomes corrupted:

```bash
# Force rebuild (deletes existing index)
python search_index.py --force
```

### Test Search from Command Line

```bash
# Test search without starting server
python search_index.py --test "Trump"
```

### Custom Index Location

Edit `search_index.py` or `search_api.py`:

```python
INDEX_DIR = Path("/custom/path/to/search_index")
```

### Increase Result Limit

Default limit is 20 results (max 100). Modify in API request:

```json
{
  "query": "search terms",
  "limit": 100
}
```

### Pagination

Use offset for pagination:

```json
{
  "query": "search terms",
  "limit": 20,
  "offset": 40  // Skip first 40 results
}
```

---

## 🔒 Legal & Ethical Guidelines

### Data Source

All documents are from **publicly released House Oversight Committee materials**. This tool does not:
- Access any private or sealed documents
- Hack, breach, or obtain documents illegally
- Contain any classified information

### Responsible Use

This tool is intended for:
- ✅ Journalistic investigation
- ✅ Academic research
- ✅ Public accountability
- ✅ Transparency advocacy
- ✅ Verification of claims

**Not intended for**:
- ❌ Harassment of individuals
- ❌ Spreading unverified claims
- ❌ Vigilante justice
- ❌ Privacy violations
- ❌ Defamation

### Evidence Standards

When using this tool for research:

1. **Cite sources** - Include document IDs and filenames
2. **Verify findings** - Cross-reference multiple documents
3. **Note limitations** - Distinguish between evidence and inference
4. **Correct errors** - Issue corrections if mistakes are found
5. **Protect victims** - Handle victim information sensitively

### Legal Disclaimer

**This tool provides search functionality only. Users are responsible for:**
- Verifying information before publication
- Complying with defamation and privacy laws
- Using findings ethically and responsibly
- Respecting victim privacy and dignity

**The creators of this tool:**
- Make no claims about the accuracy of underlying documents
- Are not responsible for user interpretations or conclusions
- Provide this tool "as is" without warranty
- Do not endorse any particular findings or theories

---

## 🤝 Contributing

Contributions are welcome! Ways to help:

### Report Issues
- Found a bug? Open an issue on GitHub
- Suggest features or improvements
- Report indexing errors or search problems

### Improve Code
- Submit pull requests with bug fixes
- Add new features (export formats, advanced queries)
- Improve documentation
- Add tests

### Extend Research
- Use tool for new investigations
- Share methodology and findings
- Cite this tool in published research
- Help verify findings from other researchers

---

## 📖 How It Works

### Indexing Process

1. **Document Discovery**: Scans `/documents` directory for .txt files
2. **Text Extraction**: Reads and cleans OCR-processed text
3. **Field Indexing**: Indexes content, document ID, and filename
4. **Schema Storage**:
   - `filepath` - Full path to document (unique ID)
   - `filename` - Original filename
   - `doc_id` - Document identifier (e.g., HOUSE_OVERSIGHT_010477)
   - `content` - Full text content (searchable)
   - `content_preview` - First 500 characters (for excerpts)
   - `file_size` - File size in bytes
   - `indexed_at` - Timestamp of indexing

### Search Process

1. **Query Parsing**: Interprets search query (AND, OR, NOT, phrases)
2. **Index Search**: Uses Whoosh's BM25F algorithm for relevance ranking
3. **Result Retrieval**: Fetches matching documents with scores
4. **Highlighting**: Marks search terms in excerpts
5. **Pagination**: Returns requested page of results

### Technology Stack

- **[Whoosh](https://whoosh.readthedocs.io/)** - Pure Python full-text search library
  - Fast indexing and searching
  - BM25F relevance ranking
  - Advanced query syntax
  - Highlighting support

- **[Flask](https://flask.palletsprojects.com/)** - Lightweight web framework
  - RESTful API endpoints
  - Web interface serving
  - JSON response formatting

---

## 🐛 Troubleshooting

### "Index not found" error

**Problem:** Search index hasn't been built yet.

**Solution:**
```bash
python search_index.py --force
```

### "No documents found" during indexing

**Problem:** Documents directory is empty or in wrong location.

**Solution:**
1. Check that `documents/` directory exists
2. Verify .txt files are present
3. Check file permissions

### "UnicodeDecodeError" during indexing

**Problem:** Document has non-UTF-8 encoding.

**Solution:** The script automatically falls back to latin-1 encoding. If problems persist, report the specific document ID.

### Search returns no results

**Problem:** Query syntax may be incorrect.

**Solution:**
- Try simpler query (single keyword)
- Check spelling
- Remove special characters
- Use phrase search: `"exact phrase"`

### Web interface not loading

**Problem:** Flask server not running or wrong port.

**Solution:**
1. Check that `python search_api.py` is running
2. Try http://127.0.0.1:5002/ (not localhost)
3. Check firewall settings

### Port already in use

**Problem:** Another service using port 5002.

**Solution:**
Edit `search_api.py`, line 678:
```python
app.run(host='127.0.0.1', port=5003, debug=True)  # Changed to 5003
```

---

## 📊 Performance

**Indexing:**
- Time: ~2-3 minutes for 2,895 documents
- Index size: ~150-200 MB
- Memory: ~500 MB during indexing

**Searching:**
- Query time: < 1 second for most queries
- Complex queries: 1-3 seconds
- Memory: ~100-200 MB during search

**Tested on:**
- MacBook Pro M1, 16GB RAM
- Ubuntu 22.04, 8GB RAM
- Windows 11, 16GB RAM

---

## 📝 Version History

### v1.0.0 (2025-11-14)
- Initial public release
- Full-text search for 2,895 documents
- Web interface with highlighting
- RESTful API
- Documentation and examples
- Research findings included

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**Summary:** You are free to:
- Use commercially
- Modify
- Distribute
- Use privately

**Requirements:**
- Include copyright notice
- Include license text

**Limitations:**
- No warranty provided
- No liability accepted

---

## 🙏 Acknowledgments

- **House Oversight Committee** for releasing the Epstein files
- **Whoosh developers** for the excellent search library
- **ICIJ** for offshore leaks database methodology
- **All researchers and journalists** working on transparency

---

## 📬 Contact

**Questions, issues, or collaboration:**
- Open an issue on GitHub
- Email: [your contact if you want to include]

**For media inquiries:**
- All findings are reproducible using this tool
- Methodology documentation included in `/analysis` directory
- Available for verification and fact-checking

---

## 🎯 Next Steps

After setting up the search tool:

1. **Explore the documents** - Try example searches
2. **Review research findings** - Read [Master Integrated Report](analysis/MASTER_INTEGRATED_REPORT_PHASES_1_2_3.md)
3. **Verify methodology** - Check reproducibility of findings
4. **Conduct your own research** - Find new connections
5. **Share discoveries** - Help advance public accountability

---

## ⚠️ Important Notes

### Why This Tool Matters

The Epstein Transparency Act is being voted on **next week** (November 18-20, 2025) in the House of Representatives. This tool demonstrates:

1. **What transparency enables** - Cross-referencing reveals hidden patterns
2. **Why full release matters** - Thousands of documents remain sealed
3. **How the public benefits** - Anyone can now search and verify
4. **What we still don't know** - Much information remains concealed

### Call to Action

If you support full transparency for the Epstein files:

1. **Contact your Representative** - https://www.house.gov/representatives/find-your-representative
2. **Share this tool** - Help others search and verify
3. **Verify findings** - Check the research documented here
4. **Demand accountability** - Use evidence for advocacy

---

**Built with transparency, for transparency.** 🔍
