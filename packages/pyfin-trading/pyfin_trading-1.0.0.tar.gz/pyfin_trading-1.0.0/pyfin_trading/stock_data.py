import yfinance as yf
from datetime import datetime, timedelta

def get_data(ticker, start_date, end_date = datetime.today().strftime("%Y-%m-%d"), interval = "1d"):
    data = yf.download(ticker, start = start_date, end = end_date, interval = interval, progress = False)
    return data

