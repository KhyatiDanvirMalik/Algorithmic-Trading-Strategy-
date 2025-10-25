import backtrader as bt
import yfinance as yf
import datetime

# 1. Create the Strategy
class DualMovingAverageStrategy(bt.Strategy):
    """
    Implements a Dual Moving Average Crossover (MAC) strategy.
    """
    # Parameters for the strategy (you can change these)
    params = (
        ('fast_ma_period', 50),  # Period for the fast moving average
        ('slow_ma_period', 200), # Period for the slow moving average
    )

    def __init__(self):
        """
        This function is called once at the start. 
        We use it to set up our indicators.
        """
        # Get the 'close' price data line
        self.dataclose = self.datas[0].close

        # Create the fast and slow simple moving averages (SMA)
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.fast_ma_period
        )
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.slow_ma_period
        )

        # Create a Crossover indicator
        # It will be +1 if fast_ma > slow_ma (buy signal)
        # It will be -1 if fast_ma < slow_ma (sell signal)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        
        # To keep track of pending orders
        self.order = None

    def log(self, txt, dt=None):
        """ Helper function for logging actions """
        dt = dt or self.datas[0].datetime.date(0)
        # print(f'{dt.isoformat()}, {txt}') # Commented out for cleaner output during backtest

    def notify_order(self, order):
        """
        This function is called when an order status changes
        (e.g., submitted, accepted, completed).
        """
        if order.status in [order.Submitted, order.Accepted]:
            # Order is active, nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}')
                pass # Keeping logs for buys/sells suppressed for cleaner output in this version
            elif order.issell():
                # self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}')
                pass # Keeping logs for buys/sells suppressed for cleaner output in this version
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset order tracker
        self.order = None

    def next(self):
        """
        This function is called on every new bar (every new day) of data.
        This is where the main trading logic lives.
        """
        # If an order is pending, do not send another one
        if self.order:
            return

        # 1. Check if we are already in the market
        if not self.position:  # self.position.size == 0
            # Not in the market, check for a buy signal
            if self.crossover > 0:  # fast_ma crossed above slow_ma
                # self.log(f'BUY CREATE, Price: {self.dataclose[0]:.2f}') # Suppressed for cleaner output
                # Create a buy order
                self.order = self.buy(size=10) # Buy 10 units/contracts

        # 2. Check if we are in the market
        else: # self.position.size > 0
            # Already in the market, check for a sell signal
            if self.crossover < 0:  # fast_ma crossed below slow_ma
                # self.log(f'SELL CREATE (Exit Position), Price: {self.dataclose[0]:.2f}') # Suppressed for cleaner output
                # Create a sell order to close the position
                self.order = self.close()

# 2. Main execution block
if __name__ == '__main__':
    # 1. Create a Cerebro (Spanish for 'brain') engine instance
    cerebro = bt.Cerebro()

    # 2. Download and Add Data
    # We will get Gold (GC=F) data from Yahoo Finance for the last 10 years
    print("Downloading 10+ years of Gold (GC=F) data... This may take a moment.")
    
    # Use yf.Ticker for a more robust data fetch that returns flat columns
    ticker = yf.Ticker('GC=F')
    data = ticker.history(
        start='2015-01-01',
        end=datetime.date.today().isoformat(),
        auto_adjust=True
    )
    
    print("Data download complete.")
    
    # Convert the yfinance data into a format backtrader understands
    # We now know 'data' has flat columns: 'Open', 'High', 'Low', 'Close', 'Volume'
    bt_data = bt.feeds.PandasData(dataname=data)
    
    # Add the data to Cerebro
    cerebro.adddata(bt_data)
    
    # 3. Add the Strategy
    cerebro.addstrategy(DualMovingAverageStrategy)

    # 4. Set Initial Capital and Commission
    start_portfolio_value = 100000.0
    cerebro.broker.setcash(start_portfolio_value)
    
    # Set a simple commission (e.g., 0.1% per trade)
    cerebro.broker.setcommission(commission=0.001) # 0.1% commission

    # Add Analyzers for Performance Evaluation
    # These will collect data during the backtest and print summaries at the end.
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio', timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')

    # 5. Run the Backtest
    print(f'Starting Portfolio Value: {start_portfolio_value:.2f}')
    strategies = cerebro.run()
    end_portfolio_value = cerebro.broker.getvalue()
    print(f'Ending Portfolio Value: {end_portfolio_value:.2f}')
    print(f'Total Profit/Loss: {end_portfolio_value - start_portfolio_value:.2f}')

    # 6. Print Analyzer Results
    print('\n--- Backtesting Results ---')
    strategy = strategies[0] # Get the first (and only) strategy instance

    # Sharpe Ratio
    sharpe_ratio = strategy.analyzers.sharpe_ratio.get_analysis()
    if sharpe_ratio is not None:
        print(f'Sharpe Ratio: {sharpe_ratio["sharperatio"]:.2f}')
    else:
        print('Sharpe Ratio: N/A (Might require more data or trades)')

    # Drawdown
    drawdown_analysis = strategy.analyzers.drawdown.get_analysis()
    print(f'Max Drawdown: {drawdown_analysis.max.drawdown:.2f}%')
    print(f'Max Drawdown Duration: {drawdown_analysis.max.len} days')

    # Returns
    returns_analysis = strategy.analyzers.returns.get_analysis()
    print(f'Total Returns: {returns_analysis["rtot"]:.2%}')
    print(f'Annualized Returns: {returns_analysis["rnorm100"]:.2f}%')

    # Trade Analyzer (useful for trade statistics)
    trade_analysis = strategy.analyzers.trade_analyzer.get_analysis()
    if trade_analysis.total.closed > 0:
        print(f'\n--- Trade Statistics ---')
        print(f'Total Trades: {trade_analysis.total.closed}')
        print(f'Wins: {trade_analysis.won.total}')
        print(f'Losses: {trade_analysis.lost.total}')
        print(f'Win Rate: {(trade_analysis.won.total / trade_analysis.total.closed) * 100:.2f}%')
        if trade_analysis.won.total > 0:
            print(f'Average Win: {trade_analysis.won.pnl.average:.2f}')
        if trade_analysis.lost.total > 0:
            print(f'Average Loss: {trade_analysis.lost.pnl.average:.2f}')
        print(f'Longs: {trade_analysis.long.total} (Won: {trade_analysis.long.won}, Lost: {trade_analysis.long.lost})')
        print(f'Shorts: {trade_analysis.short.total} (Won: {trade_analysis.short.won}, Lost: {trade_analysis.short.lost})')
    else:
        print('\nNo trades closed during the backtest period.')


    # 7. Plot the Results
    print('\nPlotting results... close the plot window to exit.')
    cerebro.plot(style='candlestick', iplot=False, volume=False) # iplot=False for non-interactive plot