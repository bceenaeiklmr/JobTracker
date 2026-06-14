# Merge today's outputs into a single file, removing duplicates and applying filters
# Script     merge.py
# License:   MIT License
# Author:    Bence Markiel (bceenaeiklmr)
# GitHub:    https://github.com/bceenaeiklmr/JobTracker
# Date       14.06.2026
# Version    0.0.3

import csv
from pathlib import Path
from datetime import datetime, timedelta
from config import OUTPUT_PATH, LOCATION_FILTERS, DATE_LOOKBACK_DAYS


def parse_date_safe(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except:
        return datetime.min
    

def matches_location(job: dict, locations: list[str]) -> bool:
    if not locations:
        return True

    job_location = (job.get("location") or "").lower()

    return any(loc.lower() in job_location for loc in locations)


def within_date_range(job_date_str: str, lookback_days: int | None) -> bool:
    if lookback_days is None:
        return True

    job_date = parse_date_safe(job_date_str)
    cutoff = datetime.now() - timedelta(days=lookback_days)

    return job_date >= cutoff


def merge_daily_outputs(output_dir: Path = None):
    if output_dir is None:
        output_dir = Path(OUTPUT_PATH)

    today_str = datetime.now().strftime("%Y-%m-%d")

    # Find all files that contain today's date
    files = list(output_dir.glob("*.csv"))
    files = [f for f in files if today_str in f.name]

    print(f"Searching in: {output_dir} for {today_str}, found {len(files)} files.")

    if not files:
        print("No files found for today.")
        return

    all_jobs = []

    # UNION
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                rows = list(reader)
    
                if not rows:
                    print(f"Empty or invalid file: {file}")
                    continue

                for row in rows:
                    if not matches_location(row, LOCATION_FILTERS):
                        continue

                    if not within_date_range(row.get("date"), DATE_LOOKBACK_DAYS):
                        continue

                    all_jobs.append(row)

        except Exception as e:
            print(f"Failed reading {file}: {e}")
            continue

    print("Jobs:", len(all_jobs))

    # Remove duplicates
    seen = set()
    unique_jobs = []

    for job in all_jobs:
        key = (job.get("id"), job.get("url"))

        if key in seen:
            continue

        seen.add(key)
        unique_jobs.append(job)

    print("Unique jobs:", len(unique_jobs))

    if not unique_jobs:
        print("No jobs after merge.")
        return

    # Sort by date (Z-A)
    unique_jobs.sort(
        key=lambda x: parse_date_safe(x.get("date")),
        reverse=True
    )

    # Write output
    out_file = output_dir / f"merged_{today_str}.csv"

    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=unique_jobs[0].keys(),
            delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(unique_jobs)

    print(f"Merged file created: {out_file}")

  
if __name__ == "__main__":
    merge_daily_outputs()