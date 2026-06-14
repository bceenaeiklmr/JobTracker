# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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

## [0.0.2] - 2026-06-08

### Added
- Headless mode support (default: enabled).
- Automatic Chrome process lifecycle handling.
- Daily merge functionality to combine multiple output files into a single file.
- Daily dataset union (merge of multiple scrape outputs).
- Duplicate removal in merged dataset via deduplication (ID + URL based).
- Base URL handling improvement: page URL templates are now normalized automatically via function (no manual `{}` handling required).

### Fixed
- Severe scraping slowdown caused by missing/empty job posting dates.

## [0.0.1] - 2026-05-30

### Features
- Scrapes all pages of a search result from the job portal.
- Extracts structured job data including: posting date, job ID, title, URL, company name, location, and work mode (e.g., Hybrid).
- Supports multiple search profiles via configuration.
- Exports results to timestamped CSV files.
- Automatically sorts jobs by posting date (newest first).
- Provides a command-line interface for execution.