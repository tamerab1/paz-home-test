# Paz Careers Job Scraper & HR Integration

A production-grade Python scraper engineered to extract, sanitize, categorize, and export job opportunities from the Paz Oil Company careers portal (paz.co.il/jobs).

---

## 🏗️ Architecture & Technical Highlights

1. Resilient HTTP Engine:
   - Persistent session pooling leveraging requests.Session.
   - Fault-tolerant retries powered by urllib3.util.retry.Retry with exponential backoff on HTTP status codes 429, 500, 502, 503, and 504.

2. Hebrew Localization & URL Decoding:
   - URL slug decoding using urllib.parse.unquote to handle Hebrew percent-encoded characters cleanly.
   - Clean UTF-8 sanitization removing trailing whitespace, linebreaks, and hidden Unicode directional control tokens.

3. Heuristic Department Mapping:
   - Accurate categorization derived directly from URL route paths (/retail/, /financial/, /executive-operations/, /operation-1/, /sales/).
   - Keyword-based fallback heuristics ensuring complete semantic department allocation without generic fallbacks.

4. Deep Crawling Engine:
   - Optional traversal flag (--deep) visiting individual posting URLs to extract comprehensive job descriptions and dates directly from internal pages.

5. Multi-Format Export & Locking Protection:
   - JSON: Clean, machine-readable UTF-8 output.
   - CSV: Configured with utf-8-sig (BOM) and csv.QUOTE_ALL for native opening in Microsoft Excel without character corruption or layout disruption. Includes automated timestamped backup handling against OS-level file lock conflicts (PermissionError).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Windows PowerShell / Linux Bash

### Installation & Environment Setup

1. Activate the project virtual environment from the root directory:
   cd HomeTest
   .\venv\Scripts\Activate.ps1

2. Navigate into the Task 2 directory and install dependencies:
   cd task2_scraping
   pip install -r requirements.txt

---

## 💻 Execution & Usage

### Rapid Scrape (Extracts list and classifies departments)
python scrape_jobs.py

### Full Deep Crawl (Fetches comprehensive job descriptions)
python scrape_jobs.py --deep

### Optional Arguments
--json-out: Path for the JSON output file (default: jobs.json)
--csv-out: Path for the CSV output file (default: jobs.csv)
--deep: Enables deep page extraction for role descriptions (default: False)
--delay: Throttle delay in seconds between consecutive requests (default: 0.3)
--timeout: Request timeout threshold in seconds (default: 15)

---

## 🧪 Automated Testing

Execute the test suite using pytest:
pytest -v

Tests cover URL unquoting, RTL character sanitization, department routing heuristics, and dataclass serialization schemas.