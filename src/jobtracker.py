# Job tracker for a well-known Hungarian job portal.
# Script     jobtracker.py
# License:   MIT License
# Author:    Bence Markiel (bceenaeiklmr)
# GitHub:    https://github.com/bceenaeiklmr/JobTracker
# Date       08.06.2026
# version    0.0.2


# Std libraries
import argparse
import csv
import time
import math
import subprocess
import random
import re
from config import OUTPUT_PATH, PROFILES
from datetime import datetime, timedelta
from pathlib import Path


# Third-party libraries
from playwright.sync_api import sync_playwright


# Constants
# The site shows 20 jobs per page, cannot be changed by URL nor manually
JOBS_PER_PAGE = 20

# Hungarian month names to numbers mapping
MONTHS = {
    "január": 1,
    "február": 2,
    "március": 3,
    "április": 4,
    "május": 5,
    "június": 6,
    "július": 7,
    "augusztus": 8,
    "szeptember": 9,
    "október": 10,
    "november": 11,
    "december": 12,
}

# Current date for reference in date parsing
TODAY = datetime.now()


# Function to resolve profile name from the configuration file
def get_profile_url(name: str):
    if name not in PROFILES:
        raise ValueError(f"Unknown profile name: {name}")
    return PROFILES[name]


# Function to convert a page-specific URL into a URL template
def normalize_profile_url(url: str):
    parts = url.split(",")
    parts[0] = re.sub(r"/\d+$", "/{}", parts[0])
    return ",".join(parts)


# Function to connect to a Chrome instance with remote debugging
def connect_browser(playwright):
    try:
        return playwright.chromium.connect_over_cdp("http://localhost:9222")
    except Exception as e:
        print(f"[WARN] Could not connect to Chrome: {e}")
        proc = start_chrome_debug()

        for i in range(10):
            try:
                return playwright.chromium.connect_over_cdp("http://localhost:9222")
            except Exception:
                time.sleep(1)

        proc.terminate()
        raise RuntimeError("Could not connect to Chrome debug instance.")


# Function to start Chrome with remote debugging enabled
def start_chrome_debug(debug=False, headless=False):
    
    # Note: the path may need to be adjusted depending on the system and Chrome installation
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = r"C:\chrome-debug"

    quiet = not debug

    args = [
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
    ]

    if headless:
        args += ["--headless=new", "--disable-gpu"]

    if quiet:
        args += [
            "--log-level=3",
            "--disable-background-networking",
        ]

    proc =subprocess.Popen(
        args,
        stdout=None if debug else subprocess.DEVNULL,
        stderr=None if debug else subprocess.DEVNULL
    )

    return proc


# Function to parse command-line arguments
def parse_args():
    # Initialize
    parser = argparse.ArgumentParser()

    # Add profile argument
    parser.add_argument(
        "profile",
        help="Profile name (e.g. Python, etc.)"
    )

    # Debug
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose Chrome logs and UI debugging"
    )

    # Non headless mode
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run with visible browser (default is headless)"
    )

    return parser.parse_args()


# Function to parse date text like "Feladva: tegnap", "Feladva: 5. június", etc.
def parse_date(text):

    # Clean date field's text
    text = text.lower().replace("feladva:", "").strip()
    text = text.replace(".", "")

    # Convert strings to actual dates
    if "tegnap" in text:
        return TODAY - timedelta(days=1)

    if "ma" in text:
        return TODAY

    # Calculate real date from month name and day
    for month, value in MONTHS.items():
        if month in text:
            d = re.search(r"(\d+)", text)
            if d:
                return datetime(TODAY.year, value, int(d.group(1)))

    return None


class Selectors:
    TILE = "a.ga-enhanced-event-click"
    DATE = "div[aria-label='feladva']"


# Function to scrape jobs from all pages given a base URL
def scrape_jobs(page, base_url, total_pages):

    # Dictionary to hold all jobs
    all_jobs = {}

    # Loop through all pages and scrape job data
    for page_num in range(1, total_pages + 1):
        print(f"Loading page {page_num}...")

        # Load the page and wait for loading
        page.goto(base_url.format(page_num))
        page.wait_for_timeout(random.uniform(4, 5) * 1000)

        # Extract the job ads
        job_tiles = page.locator(Selectors.TILE)
        date_blocks = page.locator(Selectors.DATE)

        # Temporary dictionary for current page's jobs
        jobs = {}
        job_ids = []

        # Extract the data from each job ad tile
        for i in range(job_tiles.count()):
            el = job_tiles.nth(i)

            # First extract the job ID
            job_id = el.get_attribute("data-item-id")
            if not job_id:
                continue

            # Avoid duplicates (might happen with multiple URLs)
            if job_id in all_jobs:
                continue

            # Extract the ad URL
            url = el.get_attribute("href")
            if url:
                url = url.split("?")[0]

            # Company name
            company = el.get_attribute("data-item-brand")
            if not company or company == "classified listing":
                try:
                    parent = el.locator("xpath=ancestor::div[1]")
                    company_el = parent.locator("span[aria-label='Hirdető cég']")
                    if company_el.count() > 0:
                        company = company_el.inner_text().strip()
                except:
                    company = None

            # Location
            location = None
            try:
                location = page.locator(
                    f"li[id^='detailed-job-card-{job_id}-details-location'] strong.primary-details-location"
                ).inner_text(timeout=800).strip()
            except:
                location = None

            # Work mode is detectable if "•" separator exists in the location field
            work_mode = None
            address = location

            if location and "•" in location:
                parts = location.split("•", 1)
                work_mode = parts[0].strip()
                address = parts[1].strip()

            # Store the data in the temporary dictionary (current page)
            jobs[job_id] = {
                "id": job_id,
                "company": company,
                "date": None,
                "location": address,
                "title": el.inner_text().strip(),
                "url": url,
                "work_mode": work_mode
            }

            job_ids.append(job_id)

        # Extract the posting date and assign it to each job by matching DOM order
        for i in range(date_blocks.count()):
            if i >= len(job_ids):
                break

            text = date_blocks.nth(i).inner_text()
            jobs[job_ids[i]]["date"] = parse_date(text)

        all_jobs.update(jobs)

    return list(all_jobs.values())


# Function to save data to a CSV file
def save_jobs(jobs, output_path):
    sorted_jobs = sorted(
        jobs,
        key=lambda x: x["date"] or datetime.min,
        reverse=True
    )

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")

        writer.writerow([
            "date", "id", "company", "title",
            "location", "work_mode", "url"
        ])

        for job in sorted_jobs:
            writer.writerow([
                job["date"].strftime("%Y-%m-%d") if job["date"] else "",
                job["id"],
                job["company"],
                job["title"],
                job["location"],
                job["work_mode"],
                job["url"]
            ])


# Main execution
if __name__ == "__main__":

    # Parse arguments
    args = parse_args()

    headless = not args.gui
    if headless:
        print("Running in headless mode...")
    else:
        print("Running in non-headless mode...")
    
    # Get profile URL from config
    base_url = normalize_profile_url(get_profile_url(args.profile))

    chrome_proc = None

    # Initialize Chrome in debug mode
    try:
        chrome_proc = start_chrome_debug(
            debug=args.debug,
            headless=headless
        )

        print("Chrome initialized.")

        # Connect to existing Chrome instance with remote debugging
        with sync_playwright() as p:
            browser = connect_browser(p)
            context = browser.contexts[0]
            
            # Load the first page to determine total jobs and pages
            page = context.new_page()
            page.goto(base_url.format(1))
            page.wait_for_timeout(random.uniform(5, 6) * 1000)

            # Extract total job count from the page
            html = page.content()
            match = re.search(r'(\d+)\s+álláshirdetés', html)

            total_jobs = int(match.group(1)) if match else 0
            total_pages = math.ceil(total_jobs / JOBS_PER_PAGE)

            print("Total jobs found:", total_jobs)

            jobs = scrape_jobs(page, base_url, total_pages)

        print("Total scraped:", len(jobs))

    finally:
        if chrome_proc:
            chrome_proc.terminate()
            chrome_proc.wait()
            print("Chrome exited.")

    # Save the data
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"jobs_{args.profile}_{timestamp}.csv"

    out_dir = Path(OUTPUT_PATH)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / file_name

    save_jobs(jobs, out_path)

    print("Completed.")

    
