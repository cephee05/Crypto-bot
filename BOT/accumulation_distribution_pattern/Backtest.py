'''
BTCUSD-1h-100wks-data.csv
Start                     2023-03-20 12:00:00
End                       2025-02-17 11:00:00
Duration                    699 days 23:00:00
Exposure Time [%]                    91.99405
Equity Final [$]                1043507.51536
Equity Peak [$]                  1057393.3494
Commissions [$]                   13843.56996
Return [%]                            4.35075
Buy & Hold Return [%]               239.22223
Return (Ann.) [%]                     2.24224
Volatility (Ann.) [%]                 2.81933
CAGR [%]                              2.24562
Sharpe Ratio                          0.79531
Sortino Ratio                         1.23798
Calmar Ratio                          0.91929
Max. Drawdown [%]                     -2.4391
Avg. Drawdown [%]                    -0.19383
Max. Drawdown Duration      231 days 22:00:00
Avg. Drawdown Duration        7 days 16:00:00
# Trades                                   69
Win Rate [%]                         46.37681
Best Trade [%]                       18.87366
Worst Trade [%]                     -12.23753
Avg. Trade [%]                        1.19083
Max. Trade Duration          62 days 15:00:00
Avg. Trade Duration           9 days 07:00:00
Profit Factor                         1.56675
Expectancy [%]                        1.46225
SQN                                    1.6346
Kelly Criterion                        0.1837
_strategy                 AccumDistVolumeD...
_equity_curve                             ...
_trades                       Size  EntryB...
dtype: object

BTCUSD-h4-100weeks-data.csv

Start                     2023-03-20 12:00:00
End                       2025-02-17 08:00:00
Duration                    699 days 20:00:00
Exposure Time [%]                    84.78571
Equity Final [$]                 1012731.0432
Equity Peak [$]                  1034440.7213
Commissions [$]                    4302.93104
Return [%]                             1.2731
Buy & Hold Return [%]                 245.849
Return (Ann.) [%]                     0.66088
Volatility (Ann.) [%]                 2.82647
CAGR [%]                              0.66198
Sharpe Ratio                          0.23382
Sortino Ratio                          0.3515
Calmar Ratio                          0.13413
Max. Drawdown [%]                    -4.92696
Avg. Drawdown [%]                    -0.36332
Max. Drawdown Duration      262 days 16:00:00
Avg. Drawdown Duration       18 days 13:00:00
# Trades                                   22
Win Rate [%]                         36.36364
Best Trade [%]                       25.71854
Worst Trade [%]                     -21.70386
Avg. Trade [%]                        -0.5541
Max. Trade Duration          62 days 00:00:00
Avg. Trade Duration          26 days 20:00:00
Profit Factor                         1.07141
Expectancy [%]                         0.4449
SQN                                   0.47263
Kelly Criterion                       0.08147
_strategy                 AccumDistVolumeD...
_equity_curve                             ...
_trades                       Size  EntryB...


BTCUSD-daily-150wks-data.csv 1h
Start                     2022-04-26 20:00:00
End                       2025-03-11 20:00:00
Duration                   1050 days 00:00:00
Exposure Time [%]                    95.13018
Equity Final [$]                1058910.08396
Equity Peak [$]                 1073671.52704
Commissions [$]                   16915.10428
Return [%]                            5.89101
Buy & Hold Return [%]               117.15237
Return (Ann.) [%]                     2.00777
Volatility (Ann.) [%]                 2.59629
CAGR [%]                               2.0097
Sharpe Ratio                          0.77332
Sortino Ratio                         1.19647
Calmar Ratio                          0.81865
Max. Drawdown [%]                    -2.45254
Avg. Drawdown [%]                    -0.17165
Max. Drawdown Duration      284 days 06:00:00
Avg. Drawdown Duration        8 days 07:00:00
# Trades                                   98
Win Rate [%]                         45.91837
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
