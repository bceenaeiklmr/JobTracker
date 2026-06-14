# Browser Utilities for JobTracker
# Shared Chrome/Playwright utilities
# Author:    Bence Markiel (bceenaeiklmr)
# GitHub:    https://github.com/bceenaeiklmr/JobTracker
# Date       14.06.2026
# Version    0.0.3

import subprocess
import time
from config import CHROME_PATH, CHROME_USER_DATA_DIR, CHROME_DEBUG_PORT


def connect_browser(playwright):
    """Connect to a Chrome instance with remote debugging enabled.
    
    Args:
        playwright: Playwright instance
        
    Returns:
        Browser instance connected via CDP
        
    Raises:
        RuntimeError: If connection fails after retries
    """
    
    cdp_url = f"http://localhost:{CHROME_DEBUG_PORT}"
    try:
        return playwright.chromium.connect_over_cdp(cdp_url)
    except Exception as e:
        print(f"[WARN] Could not connect to Chrome: {e}")
        proc = start_chrome_debug()
        
        for i in range(10):
            try:
                return playwright.chromium.connect_over_cdp(cdp_url)
            except Exception:
                time.sleep(1)
        
        proc.terminate()
        raise RuntimeError("Could not connect to Chrome debug instance.")


def start_chrome_debug(debug=False, headless=False):
    """Start Chrome with remote debugging enabled.
    
    Args:
        debug: enable verbose Chrome logging (default: False)
        headless: run in headless mode (default: False)
        
    Returns:
        subprocess.Popen: Chrome process
    """

    args = [
        CHROME_PATH,
        f"--remote-debugging-port={CHROME_DEBUG_PORT}",
        f"--user-data-dir={CHROME_USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
    ]
    
    if headless:
        args += ["--headless=new", "--disable-gpu"]
    
    if not debug:
        args += ["--log-level=3", "--disable-background-networking"]
    
    return subprocess.Popen(
        args,
        stdout=None if debug else subprocess.DEVNULL,
        stderr=None if debug else subprocess.DEVNULL
    )
