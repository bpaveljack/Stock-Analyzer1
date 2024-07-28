import requests
import logging
import time
import csv
from yahooquery import Ticker

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
CIK_LOOKUP_PATH = 'cik_lookup.csv'
SNP_500_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'BRK-B', 'JPM', 'JNJ'
]
NUMBER_OF_COMPANIES = 10  # For testing, reduce the number of companies

# Function to read CIK lookup from CSV
def read_cik_lookup(csv_path):
    try:
        with open(csv_path, mode='r') as infile:
            reader = csv.reader(infile)
            cik_lookup = {rows[0]: rows[1] for rows in reader}
            logging.info(f"CIK Lookup: {cik_lookup}")
            return cik_lookup
    except FileNotFoundError:
        logging.error(f"CIK lookup CSV file not found.")
        return {}

# Function to fetch market cap and earnings data
def fetch_market_cap_and_earnings(ticker):
    try:
        summary_detail = Ticker(ticker).summary_detail.get(ticker, {})
        market_cap = summary_detail.get('marketCap', None)

        earnings = Ticker(ticker).financial_data.get(ticker, {}).get('ebitda', None)
        logging.info(f"Fetched data for {ticker}: Market Cap = {market_cap}, Earnings = {earnings}")

        return market_cap, earnings
    except Exception as e:
        logging.warning(f"Error fetching data for {ticker}: {e}")
        return None, None

# Function to calculate P/E ratio and identify top 10 most undervalued stocks
def calculate_pe_ratio(cik_lookup):
    pe_ratios = {}
    for ticker, cik in cik_lookup.items():
        market_cap, earnings = fetch_market_cap_and_earnings(ticker)
        if market_cap and earnings:
            pe_ratio = market_cap / earnings if earnings > 0 else None
            if pe_ratio:
                pe_ratios[ticker] = pe_ratio
            else:
                logging.warning(f"Invalid P/E ratio for {ticker}: Market Cap = {market_cap}, Earnings = {earnings}")
        else:
            logging.warning(f"Missing market cap or earnings for {ticker}")

    sorted_pe_ratios = sorted(pe_ratios.items(), key=lambda x: x[1])
    return sorted_pe_ratios[:10]

def main():
    cik_lookup = read_cik_lookup(CIK_LOOKUP_PATH)
    sp500_tickers = SNP_500_TICKERS[:NUMBER_OF_COMPANIES]  # Manually defined tickers

    logging.info(f"Top {NUMBER_OF_COMPANIES} Companies: {sp500_tickers}")
    cik_lookup_filtered = {ticker: cik_lookup[ticker] for ticker in sp500_tickers if ticker in cik_lookup}
    logging.info(f"Top {NUMBER_OF_COMPANIES} CIKs: {list(cik_lookup_filtered.values())}")

    undervalued_stocks = calculate_pe_ratio(cik_lookup_filtered)
    logging.info("Top 10 Most Undervalued Stocks Based on P/E Ratio:")
    for stock in undervalued_stocks:
        logging.info(stock)

if __name__ == "__main__":
    main()












































