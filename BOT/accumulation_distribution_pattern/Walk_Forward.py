'''
Segment 1: Final Equity=107767.73, Expectancy=1.55%, Return=7.77%, MaxDD=-4.42%   
Segment 2: Final Equity=119989.39, Expectancy=3.65%, Return=19.99%, MaxDD=-8.74%  
Segment 3: Final Equity=68913.99, Expectancy=-4.26%, Return=-31.09%, MaxDD=-32.71%
Segment 4: Final Equity=89597.08, Expectancy=-1.43%, Return=-10.40%, MaxDD=-23.55%
Segment 5: Final Equity=125557.65, Expectancy=2.54%, Return=25.56%, MaxDD=-17.01% 

'''

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
import matplotlib.pyplot as plt


class AccumDistVolumeDeltaStrategy(Strategy):
    period = 20  # Période de lookback pour le calcul des indicateurs

    def init(self):
        # Conversion explicite en pandas Series
        high   = pd.Series(self.data.High)
        low    = pd.Series(self.data.Low)
        close  = pd.Series(self.data.Close)
        open_  = pd.Series(self.data.Open)
        volume = pd.Series(self.data.Volume)

        # Calcul de l'Accumulation/Distribution (AD)
        # Money Flow Multiplier = ((Close - Low) - (High - Close)) / (High - Low)
        mfm = ((close - low) - (high - close)) / np.maximum((high - low), 1e-6)
        mfv = mfm * volume
        ad = mfv.cumsum()
        self.ad = ad.to_numpy()

        # Moyenne mobile simple de l'AD sur "period" périodes
        self.ad_sma = ad.rolling(window=self.period).mean().to_numpy()

        # Calcul du Volume Delta : volume positif pour bougie haussière, négatif pour bougie baissière
        self.volDelta = np.where(close > open_, volume, np.where(close < open_, -volume, 0))

        # Calcul des plus hauts et plus bas sur la période pour détecter un breakout
        self.hh = high.rolling(window=self.period).max().to_numpy()  # pour LONG
        self.ll = low.rolling(window=self.period).min().to_numpy()   # pour SHORT

    def next(self):
        # Utilisation de la longueur du tableau pour déterminer l'indice de la bougie courante
        i = len(self.data.Close) - 1

        if i < self.period:
            return

        current_close = self.data.Close[i]

        # Condition d'entrée LONG
        if not self.position:
            if (current_close > self.hh[i-1] and
                self.ad[i] > self.ad_sma[i] and
                self.volDelta[i] > 0):

                risk = current_close - self.ll[i-1]
                if risk <= 0:
                    risk = 0.001  # éviter un risque nul
                tp = current_close + 2 * risk  # ratio risque/gain 1:2

                self.buy(sl=self.ll[i-1], tp=tp, size=1) 

            # Condition d'entrée SHORT
            elif (current_close < self.ll[i-1] and
                  self.ad[i] < self.ad_sma[i] and
                  self.volDelta[i] < 0):

                risk = self.hh[i-1] - current_close
                if risk <= 0:
                    risk = 0.001
                tp = current_close - 2 * risk

                self.sell(sl=self.hh[i-1], tp=tp, size=1)

data = pd.read_csv(r"C:\Users\wille\Desktop\Fevrier 2025\BTCUSD-1h-150wks-data.csv", 
                   parse_dates=['datetime'],
                   index_col='datetime')

# Function to perform Walk-Forward Optimization
def walk_forward_optimization(data, strategy, initial_cash=110000, commission=0.002, train_percent=0.4, test_percent=0.1):
    n = len(data)
    train_size = int(n * train_percent)
    test_size = int(n * test_percent)
    results = []
    equity_curves = []

    start = 0
    while start + train_size + test_size <= n:
        train_data = data.iloc[start:start + train_size]
        test_data = data.iloc[start + train_size:start + train_size + test_size]


        bt_train = Backtest(train_data, strategy, cash=initial_cash, commission=commission)
        stats_train = bt_train.run()

        # Apply the strategy with optimized parameters on the test data
        bt_test = Backtest(test_data, strategy, cash=initial_cash, commission=commission)
        stats = bt_test.run()

        equity_curve = stats['_equity_curve']['Equity']
        equity_curves.append(equity_curve.values)

        final_equity = equity_curve.iloc[-1]
        expectancy = stats['Expectancy [%]']
        avg_return = stats['Return [%]']
        max_drawdown = stats['Max. Drawdown [%]']


        results.append((final_equity, expectancy, avg_return, max_drawdown))

        start += test_size

    return results, equity_curves

results, equity_curves = walk_forward_optimization(
    data,
    AccumDistVolumeDeltaStrategy,
    initial_cash=100000,
    commission=0.002,
    train_percent=0.45,
    test_percent=0.1
)

# Affichez les résultats
print("Walk-Forward Results:")
for i, (final_equity, expectancy, avg_return, max_drawdown) in enumerate(results, start=1):
    print(f"Segment {i}: Final Equity={final_equity:.2f}, "
          f"Expectancy={expectancy:.2f}%, Return={avg_return:.2f}%, "
          f"MaxDD={max_drawdown:.2f}%")

# Exemple de tracé des courbes d'équité
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
for eq in equity_curves:
    plt.plot(eq, alpha=0.7)
plt.title("Walk-Forward Equity Curves")
plt.xlabel("Time (bars)")
plt.ylabel("Equity")
plt.show()
