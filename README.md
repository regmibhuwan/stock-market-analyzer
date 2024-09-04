# Stock Market Analyzer

## Project Overview
This Stock Market Analyzer is a Python-based financial analytics platform that fetches real-time stock data, performs various analyses, and generates insightful visualizations. The project aims to provide users with a tool to make informed decisions about stock investments based on historical performance and key financial metrics.

## Features
- Real-time data fetching for multiple stocks (AAPL, GOOGL, MSFT, AMZN)
- Calculation of key financial metrics:
  - Total Returns
  - Volatility
  - Sharpe Ratio
- Optimal portfolio allocation using Modern Portfolio Theory
- Visualization of stock trends and analysis results

## Technologies Used
- Python 3.8+
- Flask (Web Framework)
- Pandas (Data Manipulation)
- NumPy (Numerical Computations)
- Matplotlib & Seaborn (Data Visualization)
- yfinance (Yahoo Finance API wrapper)

## Project Structure
```
stock-market-analyzer/
│
├── app.py
├── data_fetcher.py
├── data_processor.py
├── data_analysis.py
├── templates/
│   └── index.html
├── static/
│   ├── price_trends.png
│   ├── returns_distribution.png
│   ├── correlation_heatmap.png
│   └── efficient_frontier.png
├── requirements.txt
└── README.md

```

## Key Findings and Insights
1. The analysis focused on four major tech stocks: Apple (AAPL), Google (GOOGL), Microsoft (MSFT), and Amazon (AMZN).
2. These tech stocks showed higher volatility but generally better returns compared to the broader market.
3. The optimal portfolio allocation suggested a diversified investment across all four stocks for the best risk-adjusted returns.
4. Apple (AAPL) consistently showed strong performance metrics, often with the highest Sharpe ratio.

## Visualizations
The project generates several plots to visualize the analysis results:

1. Stock Price Trends: Shows the historical price movements of all analyzed stocks.
2. Returns Distribution: Illustrates the distribution of returns for each stock.
3. Correlation Heatmap: Displays the correlation between different stocks' returns.
4. Efficient Frontier: Plots the efficient frontier and highlights the optimal portfolio allocation.

These plots are saved in the `static` folder and displayed on the web interface.

## Usage
1. Run the Flask application:
   ```
   python app.py
   ```
2. Open a web browser and go to `http://localhost:5000`
3. The analysis results and plots will be displayed on the webpage.

## Future Improvements
- Expand the stock selection to include more diverse sectors
- Implement additional technical indicators for more comprehensive analysis
- Add functionality for users to input custom date ranges for analysis
- Integrate real-time news sentiment analysis to factor in market sentiment

## Challenges Overcome
- Handling real-time data fetching and processing efficiently
- Implementing complex financial calculations like the Sharpe ratio and efficient frontier
- Creating an intuitive web interface to display both numerical results and visualizations

This project demonstrates proficiency in data analysis, financial modeling, and web development, showcasing the ability to create practical tools for financial decision-making.
