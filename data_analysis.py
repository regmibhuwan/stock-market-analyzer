import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.optimize import minimize
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('stock_data.db')

# List of stock symbols
symbols = ['AMZN']

# Load the data
data = {}
for symbol in symbols:
    df = pd.read_sql(f"SELECT * FROM '{symbol}_processed'", conn)
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index, utc=True)
    data[symbol] = df

conn.close()

# Function to calculate total return
def calculate_return(stock_df):
    first_price = stock_df['Close'].iloc[0]
    last_price = stock_df['Close'].iloc[-1]
    return_pct = (last_price - first_price) / first_price * 100
    return return_pct

# Calculate total returns
returns = {symbol: calculate_return(df) for symbol, df in data.items()}

# Print the returns
print(f"\nTotal Returns:")
for symbol, return_val in returns.items():
    print(f"{symbol}: {return_val:.2f}%")

# Calculate volatility
def calculate_volatility(returns):
    return returns.std() * np.sqrt(252)

volatilities = {symbol: calculate_volatility(df['Returns']) for symbol, df in data.items()}

print(f"\nAnnualized Volatility:")
for symbol, volatility in volatilities.items():
    print(f"{symbol}: {volatility:.2%}")

# Calculate Sharpe Ratio (assuming risk-free rate of 0 for simplicity)
def calculate_sharpe_ratio(returns, volatility):
    return (returns.mean() * 252) / volatility

sharpe_ratios = {symbol: calculate_sharpe_ratio(df['Returns'], volatilities[symbol]) for symbol, df in data.items()}

print(f"\nSharpe Ratio:")
for symbol, sharpe in sharpe_ratios.items():
    print(f"{symbol}: {sharpe:.2f}")

# Calculate correlation matrix
returns_df = pd.DataFrame({symbol: df['Returns'] for symbol, df in data.items()})
correlation_matrix = returns_df.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

# Function to calculate portfolio returns
def portfolio_return(weights, returns):
    return np.sum(returns.mean() * weights) * 252

# Function to calculate portfolio volatility
def portfolio_volatility(weights, returns):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

# Function to calculate portfolio Sharpe ratio
def portfolio_sharpe_ratio(weights, returns):
    return portfolio_return(weights, returns) / portfolio_volatility(weights, returns)

# Function to minimize (negative Sharpe Ratio)
def neg_sharpe_ratio(weights, returns):
    return -portfolio_sharpe_ratio(weights, returns)

# Constraint: weights must sum to 1
def constraint(weights):
    return np.sum(weights) - 1

# Optimize portfolio
num_assets = len(returns_df.columns)
initial_weights = np.array([1/num_assets] * num_assets)
bounds = tuple((0, 1) for _ in range(num_assets))
constraint = {'type': 'eq', 'fun': constraint}

result = minimize(neg_sharpe_ratio, initial_weights, args=(returns_df,), method='SLSQP', bounds=bounds, constraints=constraint)

optimal_weights = result.x

print("\nOptimal Portfolio Weights:")
for asset, weight in zip(returns_df.columns, optimal_weights):
    print(f"{asset}: {weight:.2%}")

optimal_return = portfolio_return(optimal_weights, returns_df)
optimal_volatility = portfolio_volatility(optimal_weights, returns_df)
optimal_sharpe = portfolio_sharpe_ratio(optimal_weights, returns_df)

print(f"\nOptimal Portfolio Metrics:")
print(f"Return: {optimal_return:.2%}")
print(f"Volatility: {optimal_volatility:.2%}")
print(f"Sharpe Ratio: {optimal_sharpe:.2f}")

# Monte Carlo simulation
num_simulations = 10000
simulation_results = []

for _ in range(num_simulations):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = portfolio_return(weights, returns_df)
    volatility = portfolio_volatility(weights, returns_df)
    sharpe = portfolio_sharpe_ratio(weights, returns_df)
    simulation_results.append((returns, volatility, sharpe))

simulation_results = np.array(simulation_results)

# Create a list to store all figures
figures = []

# Plot efficient frontier
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(simulation_results[:, 1], simulation_results[:, 0], c=simulation_results[:, 2], cmap='viridis')
ax.scatter(optimal_volatility, optimal_return, c='red', s=50, marker='*')
ax.set_xlabel('Volatility')
ax.set_ylabel('Return')
ax.set_title('Efficient Frontier')
plt.colorbar(scatter, label='Sharpe Ratio')
figures.append(fig)

# Plot cumulative returns
cumulative_returns = (1 + returns_df).cumprod()

fig, ax = plt.subplots(figsize=(12, 6))
for column in cumulative_returns.columns:
    ax.plot(cumulative_returns.index, cumulative_returns[column], label=column)
ax.set_title('Cumulative Returns of Stocks')
ax.set_xlabel('Date')
ax.set_ylabel('Cumulative Return')
ax.legend()
figures.append(fig)

# Function to plot with SMA
def plot_with_sma(stock_df, stock_name, short_window=50, long_window=200):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(stock_df.index, stock_df['Close'], label='Close Price')
    ax.plot(stock_df.index, stock_df['MA50'], label=f'{short_window}-day SMA')
    ax.plot(stock_df.index, stock_df['MA200'], label=f'{long_window}-day SMA')
    ax.set_title(f'{stock_name} - Closing Price and SMAs')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    return fig

# Create SMA plots for each stock
for symbol, df in data.items():
    figures.append(plot_with_sma(df, symbol))

# Display all plots
plt.show()

# Save plots to static folder
for i, fig in enumerate(figures):
    fig.savefig(f'static/plot_{i}.png')

print("\nAll plots have been saved in the 'static' folder.")

import json

# Prepare results for JSON serialization
# Prepare results for JSON serialization
results = {
    "total_returns": {symbol: f"{value:.2f}%" for symbol, value in returns.items()},
    "volatility": {symbol: f"{value:.2%}" for symbol, value in volatilities.items()},
    "sharpe_ratio": {symbol: f"{value:.2f}" for symbol, value in sharpe_ratios.items()},
    "correlation_matrix": correlation_matrix.to_dict(),
    "optimal_weights": {symbol: f"{weight:.2%}" for symbol, weight in zip(returns_df.columns, optimal_weights)},
    "optimal_portfolio": {
        "return": f"{optimal_return:.2%}",
        "volatility": f"{optimal_volatility:.2%}",
        "sharpe_ratio": f"{optimal_sharpe:.2f}"
    }
}

# Save results to a JSON file
with open('static/analysis_results.json', 'w') as f:
    json.dump(results, f)