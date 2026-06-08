# JobTracker

A CLI-based job scraping and aggregation tool for a Hungarian job portal built with Python and Playwright.

## Overview

JobTracker automates job search by collecting listings from multiple pages, extracting structured job data, and exporting it into sorted CSV files.

The main limitation of the target job portal is that search results cannot be reliably sorted by posting date. This makes manual browsing inefficient when looking for newly published listings.

## Features

- Scrapes all pages of a search result
- Extracts:
  - Posting date, job id, url
  - Company name, job title, location, work mode (hybrid)
- Supports multiple configurable search profiles
- Headless mode support (enabled by default)
- Automatic Chrome process lifecycle handling
- Daily merge functionality to combine multiple output files into a single dataset
- Command-line interface

## Installation

### Prerequisites

- Python 3.10+
- Google Chrome
- pip

### Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Install Playwright browser binaries:

```bash
playwright install
```

### Chrome Setup

The scraper connects to a running Chrome instance via remote debugging.

**Option 1: Manual Chrome Launch**

Start Chrome with remote debugging enabled:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug"
```

**Option 2: Automatic Launch** 

The script can launch Chrome automatically (see `start_chrome_debug()` in the code).

## Configuration

Edit `config.py` to define your search profiles. Each profile is a saved search URL from profession.hu.

Example:
```python
PROFILES = {
    "python": "https://www.profession.hu/allasok/budapest/...",
    "crm": "https://www.profession.hu/allasok/budapest/..."
}
```

You can create new profiles by:
1. Performing a job search on the site with your desired filters
2. Copying the URL from the browser address bar
3. Adding it to the `PROFILES` dictionary in `config.py`

Also, update the `OUTPUT_PATH` variable to specify where CSV files should be saved.

## Usage

Run the scraper with a profile name defined in `config.py`:

```bash
python jobtracker.py <profile_name>
```

Examples:

```bash
python jobtracker.py python
python jobtracker.py crm
...
python merge.py
```

The script will:
1. Launch the browser and navigate to the saved search URL
2. Scrape all pages of results
3. Parse job posting dates (including Hungarian date formats)
4. Sort jobs by posting date (newest first)
5. Export results to a CSV file with a timestamp

Sample output:
```
Total jobs found: 55
Loading page 1...
Loading page 2...
Loading page 3...
Total scraped: 55
```

## CSV Output

| date       | id     | company      | title               | location | work_mode | url                 |
|------------|--------|--------------|---------------------|----------|-----------|---------------------|
| 2026-05-31 | 100001 | Example Corp | Marketing Analyst   | Budapest | Hybrid    | https://example.com |
| 2026-05-29 | 100002 | Sample Ltd   | CRM Specialist      | Budapest | Hybrid    | https://example.com |
| 2026-05-28 | 100003 | Demo Inc     | Product Analyst     | Remote   | Remote    | https://example.com |


## Limitations

- Depends on the current HTML structure of the target site
- Changes in layout may require selector updates
- Date parsing relies on localized text formats

## Changelog

 

Details: [CHANGELOG.md](https://github.com/bceenaeiklmr/JobTracker/edit/main/CHANGELOG.md)

Latest update:

###  2026.06.08 – v0.0.2

- added headless mode support (default: enabled)
- added automatic Chrome process lifecycle handling
- added daily merge functionality to combine multiple output files into a single file
- implemented daily dataset union (merge of multiple scrape outputs)
- implemented duplicate removal in merged dataset
- base URL handling improved: page URL templates are now normalized automatically via function (no manual {} handling required)
- fixed severe scraping slowdown caused by missing/empty job posting dates
- fixed duplicate job entries in merged output via deduplication (ID + URL based)


## License

MIT License

## Author

Bence Markiel
