import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def calculate_returns(data):
    data["Daily Returns"] = data["Adj Close"].pct_change()
    data["Cumulative Returns"] = (1 + data["Daily Returns"]).cumprod()
    return data

def alpha(data, market = "^NSEI", interval = "1d", beta = 0.8, risk = 0.02):
    market_df = yf.download(market, start = data.index.min(), end = data.index.max(), interval = interval, progress = False)
    market_df['Daily Return'] = market_df['Adj Close'].pct_change()
    data['Daily Returns'] = data['Adj Close'].pct_change()
    
    # Capital Asset Pricing Model (CAPM)
    expected_return = risk + (beta * (market_df['Daily Return'].mean() - risk))

    alpha = data['Daily Returns'].mean() - expected_return
    print(f"Alpha using {market} as a proxy for the market is: {round(alpha, 3)}")


def beta(data, market = "^NSEI", interval = "1d"):
    # Nifty 50 as a proxy for the market
    market_df = yf.download(market, start = data.index.min(), end = data.index.max(), interval = interval, progress = False)
    market_df['Daily Return'] = market_df['Adj Close'].pct_change()

    covariance = data['Adj Close'].pct_change().cov(market_df['Daily Return'])
    variance_market = market_df['Daily Return'].var()

    beta = covariance / variance_market
    print(f"Beta using {market} as a proxy for the market is: {round(beta, 3)}")

def volatility(data, trading_days = 252):
    data['Daily Returns'] = data['Adj Close'].pct_change()
    data_volatility = data['Daily Returns'].std()
    annualized_volatility = data_volatility * (trading_days**0.5)
    
    print(f"Standard deviation: {round(data_volatility, 3)}")
    print(f"Annualized volatility: {round(annualized_volatility, 3)}")

def sharpe(data, risk = 0.02, trading_days = 252):
    average_return = data['Daily Returns'].mean() * trading_days
    volatility = data['Daily Returns'].std() * (trading_days**0.5)

    sharpe_ratio = (average_return - risk) / volatility
    print(f"Sharpe Ratio: {round(sharpe_ratio, 3)}")


def treynor(data, beta = 1.2, risk = 0.02, trading_days = 252):
    average_return = data['Daily Returns'].mean() * trading_days

    treynor_ratio = (average_return - risk) / beta
    print(f"Treynor Ratio: {round(treynor_ratio, 3)}")

def info(data, market = "^NSEI", interval = "1d", risk = 0.02, trading_days = 252):
    market_df = yf.download(market, start = data.index.min(), end = data.index.max(), interval = interval, progress = False)
    market_df['Daily Return'] = market_df['Adj Close'].pct_change()
    portfolio_returns = data['Daily Returns']
    benchmark_returns = market_df['Daily Return']
    portfolio_excess_return = (portfolio_returns - risk).mean() * trading_days
    benchmark_excess_return = (benchmark_returns - risk).mean() * trading_days

    tracking_error = (portfolio_returns - benchmark_returns).std() * (trading_days**0.5)
    information_ratio = (portfolio_excess_return - benchmark_excess_return) / tracking_error

    print(f"Information Ratio: {round(information_ratio, 3)}")

def sortino(data, risk = 0.02, trading_days = 252):
    portfolio_returns = data['Daily Returns']
    portfolio_excess_return = (portfolio_returns - risk).mean() * trading_days
    downside_returns = np.minimum(portfolio_returns - risk, 0)
    downside_semi_variance = (downside_returns**2).sum() / len(downside_returns)

    sortino_ratio = portfolio_excess_return / (downside_semi_variance**0.5)
    print(f"Sortino Ratio: {round(sortino_ratio, 3)}")

