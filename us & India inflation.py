# ============================================================
# US & INDIA CPI + PPI/WPI INFLATION ANALYSIS
# Fully cleaned & fixed version
# ============================================================

import requests
import pandas as pd
from bs4 import BeautifulSoup

# ---- Safe Matplotlib backend (avoids GUI errors) ----
import matplotlib
matplotlib.use("Agg")      # ensures compatibility everywhere
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# PART 1: Fetching Functions
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
    "US_PPI": get_latest_from_te_page("https://tradingeconomics.com/united-states/producer-prices-change"),
    "India_CPI": get_latest_from_te_page("https://tradingeconomics.com/india/inflation-cpi"),
    "India_WPI": get_latest_from_te_page("https://tradingeconomics.com/india/wholesale-price-index")
}

print("===== LATEST INFLATION DATA =====")
for k, v in data.items():
    print(f"{k}: {v}")


# ------------------------------------------------------------
# PART 3: Convert to DataFrame
# ------------------------------------------------------------

inflation_df = pd.DataFrame([
    ["United States", "CPI", data["US_CPI"]],
    ["United States", "PPI", data["US_PPI"]],
    ["India", "CPI", data["India_CPI"]],
    ["India", "WPI", data["India_WPI"]],
], columns=["Country", "Indicator", "Value"])

print("\n===== DATAFRAME =====")
print(inflation_df)


# ------------------------------------------------------------
# PART 4: Plot Basic Bar Chart (always works)
# ------------------------------------------------------------

plt.figure(figsize=(8, 4))
plt.bar(inflation_df["Indicator"], inflation_df["Value"].astype(str))
plt.title("US & India Inflation Indicators")
plt.xlabel("Indicator")
plt.ylabel("Latest Value")
plt.tight_layout()

plt.savefig("inflation_chart.png")   # saved safely (no GUI needed)
print("\nChart saved as: inflation_chart.png")
