TODO:

[] feed the last x to an LLM
[] scrape the relevant JD's from the individual pages
[] feed again the result to an LLM


06 11

[] Any Keywords can be used -> if not found profile, replace the keyword into the 4. param, %% text replacement req

[] Google path check function
[] Add to readme, how much time is saved actually
[] Add to readme, visual representation of the process

06 14

[x] Output folder is created in the root folder
[x] All parameter implemented to scrape all profile URLs ('all')
[x] Multiple profiles handling added (e.g., 'python analytics')
[x] Date and location filtering added, see the config file
[x] Scrapes job ads individually, stores the jd in a single string (around 2000 chars)
[x] Added time logging for each steps and jobs per second, total time
[x] Merge automatically called running the main jobtracker.py
[x] Added random delays
[x] Chrome only called once (faster for multiple profiles)