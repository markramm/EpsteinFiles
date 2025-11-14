#!/usr/bin/env python3
"""
Epstein Files Search API
Flask API for searching the House Oversight Epstein documents
"""

from flask import Flask, request, jsonify, render_template_string
from pathlib import Path
from whoosh.index import open_dir, exists_in
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh import scoring, highlight
from datetime import datetime
import re

app = Flask(__name__)

# HTML template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Epstein Files Search</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 16px;
            opacity: 0.9;
        }
        .search-section {
            padding: 30px;
            border-bottom: 1px solid #e0e0e0;
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .search-box input {
            flex: 1;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-box input:focus {
            border-color: #667eea;
        }
        .search-box button {
            padding: 12px 30px;
            font-size: 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .search-box button:hover {
            background: #5568d3;
        }
        .search-options {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .search-options label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            color: #666;
        }
        .stats {
            background: #f9f9f9;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e0e0e0;
        }
        .stats-item {
            font-size: 14px;
            color: #666;
        }
        .stats-item strong {
            color: #333;
            font-size: 16px;
        }
        .results {
            padding: 30px;
        }
        .result-item {
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }
        .result-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .result-score {
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .result-filename {
            font-size: 13px;
            color: #666;
            margin-bottom: 10px;
        }
        .result-excerpt {
            font-size: 14px;
            line-height: 1.6;
            color: #444;
        }
        .result-excerpt mark {
            background: #ffd54f;
            padding: 2px 4px;
            border-radius: 2px;
        }
        .view-doc-btn {
            display: inline-block;
            margin-top: 10px;
            padding: 6px 16px;
            background: white;
            border: 1px solid #667eea;
            color: #667eea;
            text-decoration: none;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .view-doc-btn:hover {
            background: #667eea;
            color: white;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .no-results {
            text-align: center;
            padding: 60px;
            color: #999;
        }
        .examples {
            background: #f0f4ff;
            padding: 15px 20px;
            border-radius: 6px;
            margin-top: 15px;
        }
        .examples h3 {
            font-size: 14px;
            color: #667eea;
            margin-bottom: 10px;
        }
        .examples ul {
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .examples li {
            background: white;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .examples li:hover {
            background: #667eea;
            color: white;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }
        .modal-content {
            position: relative;
            background: white;
            margin: 50px auto;
            padding: 30px;
            max-width: 900px;
            max-height: 80vh;
            overflow-y: auto;
            border-radius: 8px;
        }
        .modal-close {
            position: absolute;
            top: 15px;
            right: 15px;
            font-size: 28px;
            cursor: pointer;
            color: #999;
        }
        .modal-close:hover {
            color: #333;
        }
        .document-content {
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            background: #f9f9f9;
            padding: 20px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Epstein Files Search</h1>
            <p>Search 2,895 documents from the House Oversight Committee release</p>
        </div>

        <div class="search-section">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search documents... (e.g., 'Thiel', 'Trump AND Epstein', etc.)" />
                <button onclick="performSearch()">Search</button>
            </div>
            <div class="search-options">
                <label>
                    <input type="number" id="limitInput" value="20" min="1" max="100" style="width: 60px; padding: 5px;" />
                    results per page
                </label>
            </div>
            <div class="examples">
                <h3>Example Searches:</h3>
                <ul>
                    <li onclick="searchExample('&quot;Peter Thiel&quot;')">Peter Thiel</li>
                    <li onclick="searchExample('&quot;Steve Bannon&quot;')">Steve Bannon</li>
                    <li onclick="searchExample('Trump AND Epstein')">Trump AND Epstein</li>
                    <li onclick="searchExample('&quot;wire transfer&quot;')">Wire Transfer</li>
                    <li onclick="searchExample('Russian OR Russia')">Russian Connections</li>
                    <li onclick="searchExample('&quot;Jane Doe&quot;')">Jane Doe</li>
                </ul>
            </div>
        </div>

        <div class="stats" id="statsSection" style="display: none;">
            <div class="stats-item">
                <strong id="totalResults">0</strong> results found
            </div>
            <div class="stats-item">
                Query: <strong id="currentQuery"></strong>
            </div>
        </div>

        <div class="results" id="resultsSection"></div>
    </div>

    <div id="documentModal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle"></h2>
            <p id="modalFilename" style="color: #666; margin: 10px 0 20px 0;"></p>
            <div id="modalContent" class="document-content"></div>
        </div>
    </div>

    <script>
        function performSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) {
                alert('Please enter a search query');
                return;
            }

            const limit = document.getElementById('limitInput').value;
            const resultsSection = document.getElementById('resultsSection');
            resultsSection.innerHTML = '<div class="loading">Searching...</div>';

            fetch('/api/epstein/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    limit: parseInt(limit)
                })
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                resultsSection.innerHTML = '<div class="no-results">Error: ' + error.message + '</div>';
            });
        }

        function displayResults(data) {
            const resultsSection = document.getElementById('resultsSection');
            const statsSection = document.getElementById('statsSection');
            const totalResults = document.getElementById('totalResults');
            const currentQuery = document.getElementById('currentQuery');

            statsSection.style.display = 'flex';
            totalResults.textContent = data.total;
            currentQuery.textContent = data.query;

            if (data.total === 0) {
                resultsSection.innerHTML = '<div class="no-results">No results found for your query.</div>';
                return;
            }

            let html = '';
            data.results.forEach((result, index) => {
                const excerpt = result.excerpt
                    .replace(/<b class="match term\\d+">/g, '<mark>')
                    .replace(/<\\/b>/g, '</mark>');

                html += `
                    <div class="result-item">
                        <div class="result-header">
                            <div>
                                <div class="result-title">${index + 1}. ${result.doc_id}</div>
                                <div class="result-filename">${result.filename}</div>
                            </div>
                            <div class="result-score">Score: ${result.score.toFixed(2)}</div>
                        </div>
                        <div class="result-excerpt">${excerpt}</div>
                        <button class="view-doc-btn" onclick="viewDocument('${result.doc_id}')">
                            View Full Document
                        </button>
                    </div>
                `;
            });

            resultsSection.innerHTML = html;
        }

        function viewDocument(docId) {
            const modal = document.getElementById('documentModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalFilename = document.getElementById('modalFilename');
            const modalContent = document.getElementById('modalContent');

            modalTitle.textContent = docId;
            modalContent.innerHTML = '<div class="loading">Loading document...</div>';
            modal.style.display = 'block';

            fetch('/api/epstein/document/' + docId)
                .then(response => response.json())
                .then(data => {
                    modalFilename.textContent = data.filename;
                    modalContent.textContent = data.content;
                })
                .catch(error => {
                    modalContent.innerHTML = '<div style="color: red;">Error loading document: ' + error.message + '</div>';
                });
        }

        function closeModal() {
            document.getElementById('documentModal').style.display = 'none';
        }

        function searchExample(query) {
            document.getElementById('searchInput').value = query;
            performSearch();
        }

        // Allow Enter key to search
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });

        // Close modal on outside click
        window.onclick = function(event) {
            const modal = document.getElementById('documentModal');
            if (event.target === modal) {
                closeModal();
            }
        }
    </script>
</body>
</html>
"""

# Configuration
INDEX_DIR = Path(__file__).parent / "search_index"


class EpsteinSearcher:
    """Wrapper class for search functionality"""

    def __init__(self, index_dir):
        self.index_dir = Path(index_dir)
        if not exists_in(str(self.index_dir)):
            raise ValueError(f"Search index not found at {self.index_dir}. Run search_index.py first.")
        self.ix = open_dir(str(self.index_dir))

    def search(self, query_string, limit=20, offset=0, highlight_terms=True):
        """
        Search the index

        Args:
            query_string: Search query
            limit: Maximum results to return
            offset: Pagination offset
            highlight_terms: Whether to highlight search terms in excerpts

        Returns:
            dict with results and metadata
        """
        with self.ix.searcher(weighting=scoring.BM25F()) as searcher:
            # Parse query - search in both content and doc_id fields
            parser = MultifieldParser(
                ["content", "doc_id", "filename"],
                self.ix.schema,
                group=OrGroup
            )

            try:
                query = parser.parse(query_string)
            except Exception as e:
                return {
                    "error": f"Invalid query: {str(e)}",
                    "results": [],
                    "total": 0
                }

            # Execute search
            results = searcher.search_page(query, pagenum=(offset // limit) + 1, pagelen=limit)

            # Format results
            formatted_results = []
            for result in results:
                # Get highlighted excerpt
                if highlight_terms:
                    excerpt = result.highlights("content", top=3)
                    if not excerpt:
                        excerpt = result['content_preview'][:300] + "..."
                else:
                    excerpt = result['content_preview'][:300] + "..."

                formatted_results.append({
                    "doc_id": result['doc_id'],
                    "filename": result['filename'],
                    "filepath": result['filepath'],
                    "excerpt": excerpt,
                    "score": result.score,
                    "file_size": result.get('file_size', 0)
                })

            return {
                "query": query_string,
                "results": formatted_results,
                "total": len(results),
                "offset": offset,
                "limit": limit,
                "has_more": results.pagenum < results.pagecount
            }

    def get_document(self, doc_id):
        """
        Retrieve full document by ID

        Args:
            doc_id: Document ID (e.g., "HOUSE_OVERSIGHT_010477")

        Returns:
            Document content or None if not found
        """
        with self.ix.searcher() as searcher:
            results = searcher.documents(doc_id=doc_id)

            for result in results:
                return {
                    "doc_id": result['doc_id'],
                    "filename": result['filename'],
                    "filepath": result['filepath'],
                    "content": result['content'],
                    "file_size": result.get('file_size', 0),
                    "indexed_at": result.get('indexed_at')
                }

            return None


# Initialize searcher
try:
    searcher = EpsteinSearcher(INDEX_DIR)
except ValueError as e:
    print(f"Warning: {e}")
    searcher = None


@app.route('/api/epstein/search', methods=['POST', 'GET'])
def search_endpoint():
    """
    Search endpoint

    POST/GET /api/epstein/search
    Parameters:
        - query: Search query string (required)
        - limit: Max results (default: 20)
        - offset: Pagination offset (default: 0)
        - highlight: Highlight search terms (default: true)

    Returns:
        JSON with search results
    """
    if searcher is None:
        return jsonify({
            "error": "Search index not initialized. Run search_index.py to build index."
        }), 500

    # Get parameters
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('query')
        limit = data.get('limit', 20)
        offset = data.get('offset', 0)
        highlight = data.get('highlight', True)
    else:
        query = request.args.get('query')
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        highlight = request.args.get('highlight', 'true').lower() == 'true'

    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # Validate limits
    if limit > 100:
        limit = 100
    if offset < 0:
        offset = 0

    # Execute search
    try:
        results = searcher.search(query, limit=limit, offset=offset, highlight_terms=highlight)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500


@app.route('/api/epstein/document/<doc_id>', methods=['GET'])
def get_document_endpoint(doc_id):
    """
    Get full document by ID

    GET /api/epstein/document/<doc_id>

    Returns:
        JSON with full document content
    """
    if searcher is None:
        return jsonify({
            "error": "Search index not initialized. Run search_index.py to build index."
        }), 500

    try:
        doc = searcher.get_document(doc_id)
        if doc:
            return jsonify(doc)
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve document: {str(e)}"}), 500


@app.route('/api/epstein/stats', methods=['GET'])
def stats_endpoint():
    """
    Get index statistics

    GET /api/epstein/stats

    Returns:
        JSON with index statistics
    """
    if searcher is None:
        return jsonify({
            "error": "Search index not initialized"
        }), 500

    try:
        with searcher.ix.searcher() as s:
            doc_count = s.doc_count_all()

        return jsonify({
            "total_documents": doc_count,
            "index_path": str(INDEX_DIR)
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get stats: {str(e)}"}), 500


@app.route('/api/epstein/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok" if searcher else "no_index",
        "index_initialized": searcher is not None
    })


@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    print("=" * 70)
    print("EPSTEIN FILES SEARCH API & WEB INTERFACE")
    print("=" * 70)
    print(f"Index location: {INDEX_DIR}")
    print(f"Index exists: {exists_in(str(INDEX_DIR))}")
    print("\nWeb Interface:")
    print("  http://127.0.0.1:5002/")
    print("\nAPI Endpoints:")
    print("  GET    /                           - Web search interface")
    print("  POST   /api/epstein/search        - Search documents")
    print("  GET    /api/epstein/search        - Search documents (query params)")
    print("  GET    /api/epstein/document/<id> - Get full document")
    print("  GET    /api/epstein/stats         - Index statistics")
    print("  GET    /api/epstein/health        - Health check")
    print("=" * 70)
    print("\nStarting server on http://127.0.0.1:5002")
    print("=" * 70)

    app.run(host='127.0.0.1', port=5002, debug=True)
