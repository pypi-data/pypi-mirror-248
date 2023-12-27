import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# SMA
def sma(stock_data, sma_period = 15):
  stock_data["SMA"] = stock_data["Adj Close"].rolling(window = sma_period).mean()
  return stock_data

# EMA
def ema(stock_data, ema_period = 15, adjust = False):
  stock_data["EMA"] = stock_data["Adj Close"].ewm(span = ema_period, adjust = adjust).mean()
  return stock_data

# RSI
def rsi(stock_data, rsi_period = 14):
  delta = stock_data['Adj Close'].diff()
  gain = delta.where(delta > 0, 0)
  loss = -delta.where(delta < 0, 0)
  avg_gain = gain.rolling(window = rsi_period).mean()
  avg_loss = loss.rolling(window = rsi_period).mean()
  rs = avg_gain / avg_loss
  stock_data["RSI"] = 100 - (100 / (1 + rs))
  return stock_data

# Connors RSI
def connors_rsi(stock_data, rsi_period = 14, updown_length = 2):
  delta = stock_data['Adj Close'].diff()
  gain = delta.where(delta > 0, 0)
  loss = -delta.where(delta < 0, 0)
  avg_gain = gain.rolling(window = rsi_period).mean()
  avg_loss = loss.rolling(window = rsi_period).mean()
  rs = avg_gain / avg_loss
  stock_data["RSI"] = 100 - (100 / (1 + rs))

  stock_data['Updown'] = stock_data['Adj Close'].diff(updown_length)
  stock_data['Updown'] = stock_data['Updown'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

  stock_data['Connors_RSI'] = (stock_data['RSI'] + avg_gain + stock_data['Updown']) / 3
  return stock_data

# Stochastic Oscillator
def stoch(stock_data, k = 14, d = 3):
  stock_data["Lowest Low"] = stock_data["Low"].rolling(window = k).min()
  stock_data["Highest High"] = stock_data["High"].rolling(window = k).max()
  stock_data["%K"] = ((stock_data["Adj Close"] - stock_data["Lowest Low"]) / (stock_data["Highest High"] - stock_data["Lowest Low"])) * 100
  stock_data["%D"] = stock_data["%K"].rolling(window = d).mean()
  return stock_data

# Bollinger Bands
def bollinger_bands(stock_data, sma_period = 20, std_dev = 2):
  stock_data["SMA - BB"] = stock_data["Adj Close"].rolling(window = sma_period).mean()
  stock_data["Std Dev - BB"] = stock_data["Adj Close"].rolling(window = sma_period).std()
  stock_data["Upper Band"] = stock_data["SMA - BB"] + (stock_data["Std Dev - BB"] * std_dev)
  stock_data["Lower Band"] = stock_data["SMA - BB"] - (stock_data["Std Dev - BB"] * std_dev)
  return stock_data

# Aroon Oscillator
def aroon(stock_data, aroon_period = 25):
  stock_data["Aroon_High"] = stock_data["High"].rolling(window = aroon_period).apply(lambda x: x.argmax() + 1)
  stock_data["Aroon_Low"] = stock_data["Low"].rolling(window = aroon_period).apply(lambda x: x.argmin() + 1)
  stock_data["Aroon_Up"] = ((aroon_period - stock_data["Aroon_High"]) / aroon_period) * 100
  stock_data["Aroon_Down"] = ((aroon_period - stock_data["Aroon_Low"]) / aroon_period) * 100
  stock_data["Aroon Oscillator"] = stock_data["Aroon_Up"] - stock_data["Aroon_Down"]
  return stock_data

# Moving Average Convergence Divergence
def macd(stock_data, short_period = 12, long_period = 26, signal = 9, adjust = False):
  stock_data['Short_EMA'] = stock_data['Adj Close'].ewm(span = short_period, adjust = adjust).mean()
  stock_data['Long_EMA'] = stock_data['Adj Close'].ewm(span = long_period, adjust = adjust).mean()
  stock_data['MACD_Line'] = stock_data['Short_EMA'] - stock_data['Long_EMA']
  stock_data['Signal_Line'] = stock_data['MACD_Line'].ewm(span = signal, adjust = adjust).mean()

  stock_data['MACD_Histogram'] = stock_data['MACD_Line'] - stock_data['Signal_Line']
  return stock_data

# Ichimoku Cloud
def ichimoku_cloud(stock_data, conversion = 9, base = 26, lead_b = 52):
  stock_data['Tenkan-sen'] = (stock_data['High'].rolling(window = conversion).max() + stock_data['Low'].rolling(window = conversion).min()) / 2
  stock_data['Kijun-sen'] = (stock_data['High'].rolling(window = base).max() + stock_data['Low'].rolling(window = base).min()) / 2
  stock_data['Senkou Span A'] = ((stock_data['Tenkan-sen'] + stock_data['Kijun-sen']) / 2).shift(base)
  stock_data['Senkou Span B'] = ((stock_data['High'].rolling(window = lead_b).max() + stock_data['Low'].rolling(window = lead_b).min()) / 2).shift(base)
  stock_data['Chikou Span'] = stock_data['Adj Close'].shift(-base)
  return stock_data



