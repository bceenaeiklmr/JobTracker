# Helper timer class to track durations
# Script     timer.py
# License:   MIT License
# Author:    Bence Markiel (bceenaeiklmr)
# GitHub:    https://github.com/bceenaeiklmr/JobTracker
# Date       14.06.2026
# Version    0.0.3

import time


# Simple timer utility to analyze steps in the process
class Timer:
    def __init__(self):
        self.events = []
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()
        self.events.append(("start", self.start_time, None))

    def mark(self, name: str, count: int | None = None):
        self.events.append((name, time.perf_counter(), count))

    def report(self):
        if len(self.events) < 2:
            return {}

        durations = []

        for i in range(1, len(self.events)):
            name = self.events[i][0]
            duration = self.events[i][1] - self.events[i - 1][1]
            durations.append((name, duration))

        total = self.events[-1][1] - self.events[0][1]
        avg = total / (len(self.events) - 1)

        # sum counts if available
        total_jobs = sum(e[2] for e in self.events if e[2] is not None)

        jobs_per_second = None

        if total_jobs:
            jobs_per_second = total / total_jobs

        return {
            "total_time": total,
            "avg_time": avg,
            "steps": durations,
            "total_jobs": total_jobs if total_jobs else None,
            "jobs_per_second": jobs_per_second
        }

    def print_report(self):
        report = self.report()

        print("\nTiming report:")
        print(f"Total time: {report['total_time']:.2f}s")
        print(f"Avg step time: {report['avg_time']:.2f}s")

        if report.get("total_jobs") is not None:
            print(f"Total jobs: {report['total_jobs']}")
            print(f"Jobs per second: {report['jobs_per_second']:.2f}")

        for name, t in report["steps"]:
            print(f"+ {name}: {t:.2f}s")