# JobTracker

A Python-based CLI tool for scraping, aggregating, and analyzing job listings from a Hungarian job portal using Playwright.

## Overview

JobTracker automates job discovery by collecting listings across multiple search profiles and pages, extracting structured job data, and exporting it into clean, deduplicated datasets.

Since the target job portal does not provide reliable sorting by posting date, JobTracker focuses on programmatic collection and post-processing the most relevant and recent listings efficiently.

## Features

- Multi-page scraping with full pagination support
- Multi-profile search execution (e.g. multiple keywords or job categories)
- Structured data extraction:
  - Job ID, URL
  - Posting date
  - Company name
  - Job title
  - Location
  - Work mode (e.g. hybrid/remote)
- Configurable filtering:
  - Date-based filtering (e.g. last N days)
  - Location-based filtering
- Automatic deduplication of job listings
- Aggregation and merge of daily outputs into a unified dataset
- CLI-based execution flow
- Headless browser support (Playwright + Chrome lifecycle management)
- Performance tracking (execution time, jobs per second)
- Randomized delays to reduce request patterns and improve stability

## Output

- Tab-separated CSV exports per run
- Daily merged dataset generation
- Optional structured enrichment of job descriptions (JD aggregation)

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

### Filtering
`[] or None = no filter`
```bash
LOCATION_FILTERS = ["Budapest", "Budaörs"]
```

`None = no filter`
```bash
DATE_LOOKBACK_DAYS = 7
```

## Usage

Run the scraper with a profile name defined in `config.py`:

```bash
python jobtracker.py <profile_name>

# Examples:
python jobtracker.py python

# or multiple profile names
python jobtracker.py python crm

# or all profile names
python jobtracker.py all

# optional job description download
python jobad.py <csv_path>
```

The script performs the following:

1. Launches a Playwright-controlled browser and navigates to configured search profiles
2. Iterates through all result pages and collects job listings
3. Extracts structured job data including:
   - Job ID and URL
   - Posting date (including Hungarian date formats)
   - Company name, job title, location, and work mode
4. Applies configurable filtering:
   - Date-based filtering (e.g. last N days)
   - Location-based filtering
5. Deduplicates job entries across pages and profiles
6. Aggregates and sorts results by posting date (newest first)
7. Exports results into tab-separated CSV files
8. Optionally merges daily outputs into a single consolidated dataset

Sample output:
```bash
Total jobs found: 55
Loading page 1...
Loading page 2...
Loading page 3...
Total scraped: 55
```

```bash
Searching in: output for 2026-06-14, found 15 files.
Jobs: 246
Unique jobs: 106
Merged file created: output\merged_2026-06-14.csv

Timing report:
Total time: 38.65s
Avg step time: 12.88s
Total jobs: 42
Jobs per second: 0.92
+ test: 12.64s
+ vba: 21.71s
+ merge: 4.29s
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

Latest updates:

## [0.0.3] - 2026-06-14

- Output folder is created in the project root directory
- Added support for scraping all profile URLs using the `all` parameter
- Implemented multi-profile handling (e.g. `"python analytics"`)
- Added date and location filtering (configurable via `config.py`)
- Job descriptions can be scraped individually and stored as a single string (~2000 characters), see jobad.py
- Added execution time tracking per step, including jobs-per-second and total runtime metrics
- Automatic merge process integrated into `jobtracker.py`
- Introduced random delays between requests to reduce request intensity
- Browser instance is reused across multiple profiles

###  2026.06.08 - v0.0.2

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
