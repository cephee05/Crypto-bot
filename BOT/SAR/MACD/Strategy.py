'''
Start                     2023-03-21 12:00:00
End                       2025-02-18 12:00:00
Duration                    700 days 00:00:00
Exposure Time [%]                    23.94668
Equity Final [$]                  120970.6852
Equity Peak [$]                  124040.62984
Commissions [$]                     8267.6348
Return [%]                            9.97335
Buy & Hold Return [%]                 46.3262
Return (Ann.) [%]                      5.0746
Volatility (Ann.) [%]                11.31608
CAGR [%]                              5.08203
Sharpe Ratio                          0.44844
Sortino Ratio                         0.83249
Calmar Ratio                           0.6217
Max. Drawdown [%]                    -8.16249
Avg. Drawdown [%]                    -3.55767
Max. Drawdown Duration      244 days 04:00:00
Avg. Drawdown Duration       55 days 03:00:00
# Trades                                   49
Win Rate [%]                         48.97959
Best Trade [%]                       25.78424
Worst Trade [%]                      -7.60714
Max. Trade Duration           6 days 16:00:00
Avg. Trade [%]                        0.80961
Profit Factor                          1.6156
Expectancy [%]                        0.98964
SQN                                    1.1006
Kelly Criterion                       0.18522
_strategy                    PSARMACDStrategy
_equity_curve                             ...
_trades                       Size  EntryB...
'''

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class PSARMACDStrategy(Strategy):
    order_value = 1000  # Ordre fixé à 1000 dollars
    psar_start = 0.01
    psar_step  = 0.01
    psar_max   = 0.1

    ema_length = 200

    macd_fast  = 24
    macd_slow  = 52
    macd_signal= 18

    def init(self):
        close_s = pd.Series(self.data.Close, index=self.data.index)
        high_s  = pd.Series(self.data.High,  index=self.data.index)
        low_s   = pd.Series(self.data.Low,   index=self.data.index)

        # Parabolic SAR
        psar_arr = talib.SAR(
            high_s, low_s, 
            acceleration=self.psar_step, 
            maximum=self.psar_max
        )
        self.psar = self.I(lambda: psar_arr, name='PSAR')

        # EMA for trend filter
        ema_arr = talib.EMA(close_s, timeperiod=self.ema_length)
        self.ema = self.I(lambda: ema_arr, name=f'EMA({self.ema_length})')

        # MACD: returns macd, signal, hist
        macd_line, macd_signal_line, macd_hist = talib.MACD(
            close_s, 
            fastperiod=self.macd_fast, 
            slowperiod=self.macd_slow, 
            signalperiod=self.macd_signal
        )
        self.macd_line = self.I(lambda: macd_line, name='MACD_line')
        self.macd_sig  = self.I(lambda: macd_signal_line, name='MACD_signal')
        self.macd_hist = self.I(lambda: macd_hist, name='MACD_hist')

    def next(self):
        if len(self.data) < 2:
            return

        price_prev = self.data.Close[-2]
        price_curr = self.data.Close[-1]
        psar_prev  = self.psar[-2]
        psar_curr  = self.psar[-1]

        # PSAR flips
        flip_bullish = (psar_prev > price_prev) and (psar_curr < price_curr)
        flip_bearish = (psar_prev < price_prev) and (psar_curr > price_curr)

        # Trend filter via EMA
        ema_val = self.ema[-1]
        trend_is_up   = price_curr > ema_val
        trend_is_down = price_curr < ema_val

        # MACD cross
        macd_now  = self.macd_line[-1]
        macd_prev = self.macd_line[-2]
        sig_now   = self.macd_sig[-1]
        sig_prev  = self.macd_sig[-2]

        bullish_macd_cross = (macd_prev < sig_prev) and (macd_now > sig_now)
        bearish_macd_cross = (macd_prev > sig_prev) and (macd_now < sig_now)

        if not self.position:
            # Calcul de la taille d'ordre pour investir 1000 dollars
            size = self.order_value / price_curr

            # Go long si tendance haussière, MACD bullish et PSAR sous le prix
            if trend_is_up and bullish_macd_cross and (psar_curr < price_curr):
                self.buy(size=size)
            # Go short si tendance baissière, MACD bearish et PSAR au-dessus du prix
            elif trend_is_down and bearish_macd_cross and (psar_curr > price_curr):
                self.sell(size=size)
        else:
            # Ferme la position si le PSAR flip se produit dans le sens opposé
            if (self.position.is_long and flip_bearish) or \
               (self.position.is_short and flip_bullish):
                self.position.close()

# Chargement des données
data = pd.read_csv(
    r"C:\Users\wille\Desktop\Fevrier 2025\data\ETHUSD-h4-data.csv",  
    parse_dates=['datetime'],
    index_col='datetime'
)
    
bt = Backtest(data, PSARMACDStrategy, cash=110000, commission=0.002)

stats = bt.run()
print(stats)
bt.plot(resample=False)
