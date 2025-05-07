import pandas as pd
import numpy as np
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import matplotlib.pyplot as plt

# Load the data
#data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\BTCUSD-5m-100wks-data.csv'#BTC5min
data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\BTCUSD-15m-150wks-data.csv'  # BTC 15 min
#data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\BTCUSD-1h-150wks-data.csv'  # BTC 1 hr
#data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\BTCUSD-1h-150wks-data-H4.csv'    # BTC 4 hr
# data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\SOLUSD-15m-100wks-data.csv'  # SOL 15 min
# data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\SOLUSD-1h-150wks-data.csv'  # SOL 1 hr
# data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\ETHUSD-1h-150wks-data.csv'  # ETH 1 hr
# data_path = r'C:\Users\wille\Desktop\DATA\crypto_data\stock_data\ETHUSD-5m-100wks-data.csv' # ETH 5 min

data = pd.read_csv(data_path, parse_dates=['datetime'], index_col='datetime')

class MAReversalStrategy(Strategy):
    # Define the parameters we'll optimize
    ma_fast     = 20
    ma_slow     = 40
    take_profit = 0.10  # 10%
    stop_loss   = 0.10  # 10%

    def init(self):
        # Calculate moving averages using TA-Lib
        self.sma_fast = self.I(talib.SMA, self.data.Close, self.ma_fast)
        self.sma_slow = self.I(talib.SMA, self.data.Close, self.ma_slow)

        # Add indicators to the plot – fixed lambda functions
        self.I(lambda x: self.sma_fast, f'SMA{self.ma_fast}', overlay=True)
        self.I(lambda x: self.sma_slow, f'SMA{self.ma_slow}', overlay=True)

    def next(self):
        price = self.data.Close[-1]

        # Check for short setup: price above SMA20 but below SMA40 and not self.position
        if price > self.sma_fast[-1] and price < self.sma_slow[-1] and not self.position:
            self.sell(
                size=1,
                sl=price * (1 + self.stop_loss),
                tp=price * (1 - self.take_profit)
            )

        # Check for long setup: price above both SMAs and not self.position
        elif price > self.sma_fast[-1] and price > self.sma_slow[-1] and not self.position:
            self.buy(
                size=1,
                sl=price * (1 - self.stop_loss),
                tp=price * (1 + self.take_profit)
            )

        # Close short if price moves above SMA40
        elif self.position and self.position.is_short and price > self.sma_slow[-1]:
            self.position.close()

# Rename columns to match Backtesting.py requirements
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Sort index in ascending order to fix the warning
data = data.sort_index(ascending=True)

# Create and run the backtest with initial parameters
bt = Backtest(data, MAReversalStrategy, cash=110000, commission=0.002)

# Run backtest with default parameters
print("\n🌙 Cephee's Initial Backtest Results 🚀")
print("=" * 50)
stats = bt.run()
print(stats)

# Plot the unoptimized strategy results (close plot to continue...)
print("\n📈 Showing plot for unoptimized strategy (close plot to continue...)")
bt.plot(filename=None)
plt.show()
