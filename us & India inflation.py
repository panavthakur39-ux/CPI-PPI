# ============================================================
# FULL AUTOMATED SCRIPT: US & INDIA CPI + PPI/WPI INFLATION
# 1. Fetch latest inflation data (API + web scraping fallback)
# 2. Convert into DataFrames
# 3. Plot CPI & PPI/WPI trends
# ============================================================

import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# PART 1: FETCHING FUNCTIONS
# ------------------------------------------------------------

# ---- (A) TradingEconomics API function ----
API_KEY = ""   # OPTIONAL – Add your key if you have one

def get_te_api(country, indicator):
    """Get historical data from TradingEconomics API."""
    if API_KEY == "":
        return None  # Skip if no API key provided
    url = f"https://api.tradingeconomics.com/historical/country/{country}/indicator/{indicator}?client={API_KEY}"
    res = requests.get(url)
    if res.status_code == 200:
        return pd.DataFrame(res.json())
    return None

# ---- (B) Web scraping fallback ----
def get_latest_from_te_page(url):
    """Scrape the latest inflation number from TradingEconomics HTML page."""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        value = soup.find("td", {"class": "datatable-item"}).text.strip()
        return value
    except:
        return None

# ------------------------------------------------------------
# PART 2: FETCH LATEST VALUES (US + INDIA)
# ------------------------------------------------------------

latest_data = {
    "US_CPI": get_latest_from_te_page("https://tradingeconomics.com/united-states/inflation-cpi"),
    "US_PPI": get_latest_from_te_page("https://tradingeconomics.com/united-states/producer-prices-change"),
    "India_CPI": get_latest_from_te_page("https://tradingeconomics.com/india/inflation-cpi"),
    "India_WPI": get_latest_from_te_page("https://tradingeconomics.com/india/wholesale-price-index")
}

print("===== LATEST INFLATION DATA (US & INDIA) =====")
for k, v in latest_data.items():
    print(f"{k}: {v}")

# ------------------------------------------------------------
# PART 3: SAVE TO DATAFRAME
# ------------------------------------------------------------

inflation_df = pd.DataFrame([
    ["United States", "CPI", latest_data["US_CPI"]],
    ["United States", "PPI", latest_data["US_PPI"]],
    ["India", "CPI", latest_data["India_CPI"]],
    ["India", "WPI", latest_data["India_WPI"]],
], columns=["Country", "Indicator", "Value"])

print("\n===== DATAFRAME =====")
print(inflation_df)

# ------------------------------------------------------------
# PART 4: HISTORICAL TREND PLOTTING (If API Key Provided)
# ------------------------------------------------------------

if API_KEY != "":
    print("\nFetching historical data using API...")

    us_cpi_hist = get_te_api("united states", "inflation rate")
    us_ppi_hist = get_te_api("united states", "producer prices change")
    india_cpi_hist = get_te_api("india", "inflation rate")
    india_wpi_hist = get_te_api("india", "wholesale price index inflation yoy")

    if us_cpi_hist is not None:
        # Convert 'DateTime' to actual dates
        us_cpi_hist["DateTime"] = pd.to_datetime(us_cpi_hist["DateTime"])
        india_cpi_hist["DateTime"] = pd.to_datetime(india_cpi_hist["DateTime"])

        # ----------------- Plot CPI Trend --------------------
        plt.figure(figsize=(10,5))
        plt.plot(us_cpi_hist["DateTime"], us_cpi_hist["Value"], label="US CPI")
        plt.plot(india_cpi_hist["DateTime"], india_cpi_hist["Value"], label="India CPI")
        plt.title("CPI Trend: United States vs India")
        plt.xlabel("Year")
        plt.ylabel("Inflation Rate (%)")
        plt.legend()
        plt.grid(True)
        plt.show()

        # ----------------- Plot PPI/WPI Trend ----------------
        if us_ppi_hist is not None and india_wpi_hist is not None:
            us_ppi_hist["DateTime"] = pd.to_datetime(us_ppi_hist["DateTime"])
            india_wpi_hist["DateTime"] = pd.to_datetime(india_wpi_hist["DateTime"])

            plt.figure(figsize=(10,5))
            plt.plot(us_ppi_hist["DateTime"], us_ppi_hist["Value"], label="US PPI")
            plt.plot(india_wpi_hist["DateTime"], india_wpi_hist["Value"], label="India WPI")
            plt.title("PPI/WPI Trend: United States vs India")
            plt.xlabel("Year")
            plt.ylabel("Producer/Wholesale Inflation (%)")
            plt.legend()
            plt.grid(True)
            plt.show()

    else:
        print("⚠ No API key provided – skipping trend charts.")
else:
    print("\n⚠ API key not provided – trend charts not downloaded.")
