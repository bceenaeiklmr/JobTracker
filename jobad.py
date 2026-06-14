# Job description flattener for JobTracker
# Script     jobad.py
# License:   MIT License
# Author:    Bence Markiel (bceenaeiklmr)
# GitHub:    https://github.com/bceenaeiklmr/JobTracker
# Date       14.06.2026
# Version    0.0.3

import argparse
import csv
import re
import sys
import random
from config import OUTPUT_PATH
from datetime import datetime
from pathlib import Path


# Third-party libraries
from playwright.sync_api import sync_playwright

# Shared utilities
from browser_utils import connect_browser, start_chrome_debug


# Constants
JD_PRIMARY_SELECTOR = "#column_1"
JD_FALLBACK_SELECTOR = ".custom-template"
JOB_UNAVAILABLE_LABEL = "Unavailable"
JOB_UNAVAILABLE_MESSAGE = "Sajnos a keresett álláshirdetés már nem elérhető."

def flatten_jd(text):
    if not text:
        return ""
    
    # Split the raw text block into individual lines
    lines = text.split("\n")
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Clean bullet points, dashes, and trailing characters from the start of the line
        line = re.sub(r"^[\s\-•*+\:–]+", "", line).strip()
        if not line:
            continue
            
        # Ensure the first character of the sentence is capitalized
        line = line[0].upper() + line[1:]
        
        # Force a trailing punctuation mark if missing
        if not line.endswith(('.', '!', '?')):
            line += '.'
            
        processed_lines.append(line)
        
    # Join all formatted lines into a single string separated by spaces
    return " ".join(processed_lines)

def parse_args():
    parser = argparse.ArgumentParser(description="Scrape and flatten JDs from column_1 or custom templates.")
    parser.add_argument("csv_file", help="Path to the scraped jobs CSV file")
    parser.add_argument("--gui", action="store_true", help="Run with visible browser")
    parser.add_argument("--debug", action="store_true", help="Enable verbose logs")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    headless = not args.gui
    csv_path = Path(args.csv_file)
    
    if not csv_path.exists():
        print(f"[ERROR] Input file does not exist: {csv_path}")
        sys.exit(1)

    jobs_to_process = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        for row in reader:
            jobs_to_process.append(row)

    print(f"Loaded {len(jobs_to_process)} jobs.")
    chrome_proc = None
    extended_jobs = []

    try:
        chrome_proc = start_chrome_debug(debug=args.debug, headless=headless)
        with sync_playwright() as p:
            browser = connect_browser(p)
            page = browser.contexts[0].new_page()

            for idx, job in enumerate(jobs_to_process, 1):
                url = job.get("url")
                print(f"[{idx}/{len(jobs_to_process)}] Scraping: {url}")
                try:
                    # Set a 20-second timeout for pages that load slowly
                    page.goto(url, timeout=20000)
                    page.wait_for_timeout(random.uniform(2, 4) * 1000)
                    
                    # Check if the job listing is explicitly unavailable or deleted
                    page_content = page.locator("body").inner_text()
                    if JOB_UNAVAILABLE_MESSAGE in page_content:
                        extended_jobs.append({**job, "description": JOB_UNAVAILABLE_LABEL})
                        continue

                    # Try primary container first
                    jd_locator = page.locator(JD_PRIMARY_SELECTOR)

                    # Fallback to custom template container if primary is not found
                    if jd_locator.count() == 0 or not jd_locator.inner_text().strip():
                        jd_locator = page.locator(JD_FALLBACK_SELECTOR)

                    if jd_locator.count() > 0:
                        full_text = jd_locator.inner_text().strip()
                        flat_text = flatten_jd(full_text)
                    else:
                        flat_text = ""

                    extended_jobs.append({**job, "description": flat_text})
                except Exception as e:
                    print(f"[ERROR] {url}: {e}")
                    extended_jobs.append({**job, "description": ""})

    finally:
        if chrome_proc:
            chrome_proc.terminate()

    # Add the description column to the output structure
    new_fieldnames = list(fieldnames) + ["description"]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    out_path = Path(OUTPUT_PATH) / f"ads_{timestamp}.csv"

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames, delimiter="\t")
        writer.writeheader()
        for job in extended_jobs:
            writer.writerow(job)

    print(f"Completed. Output: {out_path}")