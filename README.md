Algorithmic Trading Strategy - Gold
Project Description
This project is a Python-based algorithmic trading bot designed to analyze and backtest a strategy on the gold commodity market (GC=F).

It implements a Dual Moving Average Crossover (MAC) strategy to identify market trends and generate trading signals. The system uses the backtrader library to simulate trades against historical data from yfinance.

The primary goal is to evaluate the strategy's performance based on key metrics, including profitability, risk, and maximum drawdown.

Features
Strategy: Implements a Dual Moving Average Crossover with a 50-day fast moving average and a 200-day slow moving average.

Backtesting Engine: Utilizes the backtrader library for robust and fast vectorized backtesting.

Free Data: Fetches over 10 years of historical Gold (GC=F) commodity data from Yahoo Finance using the yfinance library.

Performance Analysis: Automatically calculates and reports key metrics:

Total Profit/Loss

Annualized Returns

Sharpe Ratio

Maximum Drawdown (Risk)

Trade Statistics (Total Trades, Win Rate, etc.)

Visualization: Generates a candlestick chart using matplotlib to visualize the price data, moving averages, and all buy/sell trades.

Dependency Management: Includes a requirements.txt file for a clean and easy setup in a Python virtual environment.

Technology Stack
Python 3.x

backtrader

yfinance

matplotlib

Project Structure
algo_trader/
├── venv/                 # Python virtual environment
├── requirements.txt      # Project dependencies
└── main.py               # Main Python script


Steps to Execute
Follow these steps to set up and run the project locally.

1. Set Up the Project Directory
Create a folder for the  project and navigate into it using  terminal.

mkdir algo_trader
cd algo_trader

2. Create and Activate Virtual Environment
Create a Python virtual environment to keep dependencies isolated.

python -m venv venv
Activate the environment:
On Windows (cmd.exe / PowerShell):
venv\Scripts\activate

On macOS/Linux (bash):
source venv/bin/activate

Your terminal prompt should now show (venv).

3. Create Project Files
Create the following two files inside your algo_trader directory.

requirements.txt (This file lists all the free libraries the project needs.)
backtrader
yfinance
matplotlib
main.py (This is the main script.)

4. Install Dependencies
With the virtual environment still active, install the required libraries from the requirements.txt file.

Bash

pip install -r requirements.txt


5. Run the Backtest
Execute the main Python script from the terminal.

python main.py


6. Analyze the Output
The script will first print "Downloading 10+ years of Gold (GC=F) data..." This may take a moment.

Once complete, One will see two outputs:

In the Terminal: A complete performance report will be printed. This includes:

Starting and Ending Portfolio Value

Total Profit/Loss

Sharpe Ratio

Maximum Drawdown (e.g., Max Drawdown: 25.84%)

Annualized Returns

Trade Statistics (Win Rate, Total Trades, etc.)



<img width="1212" height="698" alt="Screenshot 2025-10-25 105452" src="https://github.com/user-attachments/assets/97ca586f-ca23-4f63-a51a-d8ce78ae0bc9" />

In a New Window: A matplotlib plot will open. This chart will show the Gold price, your 50/200-day moving averages, and all the buy (green triangles) and sell (red triangles) trades executed by the strategy.

<img width="1919" height="1125" alt="image" src="https://github.com/user-attachments/assets/f711ee6d-4031-4009-af11-2b274fd79b9c" />

