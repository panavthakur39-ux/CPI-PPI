# ============================================================
# US & INDIA CPI + PPI/WPI INFLATION (NO CHART VERSION)
# Clean, safe, error-free code
# ============================================================

import requests
import pandas as pd
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# PART 1: Function to Scrape Latest Inflation Values
# ------------------------------------------------------------

def get_latest_from_te_page(url):
    """Scrape the latest inflation number from TradingEconomics HTML page."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        value = soup.find("td", {"class": "datatable-item"}).text.strip()
        return value
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return None

# ------------------------------------------------------------
# PART 2: Fetch Latest Inflation for US & India
# ------------------------------------------------------------

print("Fetching latest CPI & PPI/WPI inflation data...\n")

data = {
    "US_CPI": get_latest_from_te_page("https://tradingeconomics.com/united-states/inflation-cpi"),
    "US_PP_
