# Profiles
PROFILES = {
  "marketing": "https://www.profession.hu/allasok/online-marketing/1,12,0,0,219",
  "crm": "https://www.profession.hu/allasok/budapest/1,0,23,crm%20elemz%c5%91,0,0,67,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,1",
  "marketing_hybrid": "https://www.profession.hu/allasok/marketing-media-pr/budapest/1,12,23,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5",
  "erp": "https://www.profession.hu/allasok/1,0,0,erp,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5",
  "python": "https://www.profession.hu/allasok/budapest/1,0,23,python,0,0,0,0,0,0,0,0,0,16",
  "dynamics": "https://www.profession.hu/allasok/budapest/1,0,23,microsoft%20dynamics%401%401?keywordsearch",
  "market_research": "https://www.profession.hu/allasok/piacelemzo-piackutato/1,12,0,0,44",
  "e-commerce": "https://www.profession.hu/allasok/budapest/1,0,0,e-commerce%401%401?keywordsearch",
  "vba": "https://www.profession.hu/allasok/1,0,0,vba",
  "test": "https://www.profession.hu/allasok/divat-stilustervezo/1,12,0,0,212"
}

# [] or None = no filter
LOCATION_FILTERS = ["Budapest", "Budaörs"]

# None - no filter
DATE_LOOKBACK_DAYS = 7

# Output folder
OUTPUT_PATH = "output"

# Chrome configuration
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_USER_DATA_DIR = r"C:\chrome-debug"
CHROME_DEBUG_PORT = 9222