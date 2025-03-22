'''
Start                     2022-04-26 20:00:00
End                       2025-03-11 20:00:00
Duration                   1050 days 00:00:00
Exposure Time [%]                    95.13018
Equity Final [$]                 168910.08396
Equity Peak [$]                  183671.52704
Commissions [$]                   16915.10428
Return [%]                           53.55462
Buy & Hold Return [%]               117.15237
Return (Ann.) [%]                    16.06116
Volatility (Ann.) [%]                20.89715
CAGR [%]                             16.07763
Sharpe Ratio                          0.76858
Sortino Ratio                         1.38484
Calmar Ratio                          1.12029
Max. Drawdown [%]                   -14.33658
Avg. Drawdown [%]                    -1.21031
Max. Drawdown Duration      284 days 06:00:00
Avg. Drawdown Duration        8 days 07:00:00
# Trades                                   98
Win Rate [%]                         44.89796
Best Trade [%]                       28.56627
Worst Trade [%]                     -16.69596
Avg. Trade [%]                        1.23125
Max. Trade Duration          81 days 12:00:00
Avg. Trade Duration          10 days 04:00:00
Profit Factor                         1.53896
Expectancy [%]                        1.60463
SQN                                   1.75204
Kelly Criterion                       0.16367
_strategy                 AccumDistVolumeD...
_equity_curve                             ...
_trades                       Size  EntryB...
dtype: object
'''

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

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


bt = Backtest(data, AccumDistVolumeDeltaStrategy, cash=110000, commission=0.002)
stats = bt.run()
print(stats)
bt.plot(resample=False)
