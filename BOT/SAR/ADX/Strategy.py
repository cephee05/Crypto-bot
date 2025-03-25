'''
Start                     2023-03-21 12:00:00
End                       2025-02-18 12:00:00
Duration                    700 days 00:00:00
Exposure Time [%]                    26.06522
Equity Final [$]                   5433.77802
Equity Peak [$]                    6011.98562
Commissions [$]                     181.73198
Return [%]                            8.67556
Buy & Hold Return [%]                54.31051
Return (Ann.) [%]                     4.42713
Volatility (Ann.) [%]                22.11705
CAGR [%]                              4.43359
Sharpe Ratio                          0.20017
Sortino Ratio                         0.32421
Calmar Ratio                          0.18567
Max. Drawdown [%]                   -23.84358
Avg. Drawdown [%]                    -4.01763
Max. Drawdown Duration      560 days 00:00:00
Avg. Drawdown Duration       41 days 18:00:00
# Trades                                   14
Win Rate [%]                             50.0
Best Trade [%]                       40.89945
Worst Trade [%]                     -12.02245
Avg. Trade [%]                        1.14395
Max. Trade Duration          33 days 08:00:00
Avg. Trade Duration          12 days 21:00:00
Profit Factor                         1.61239
Expectancy [%]                        1.83692
SQN                                   0.43711
Kelly Criterion                       0.15505
'''

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class PSARADXStrategy(Strategy):
    psar_start = 0.01
    psar_step  = 0.01
    psar_max   = 0.01

    adx_period = 14

    def init(self):
        # Convert data for TA-Lib
        high_series = pd.Series(self.data.High, index=self.data.index)
        low_series  = pd.Series(self.data.Low,  index=self.data.index)
        close_series= pd.Series(self.data.Close,index=self.data.index)

        # PSAR
        psar_arr = talib.SAR(
            high_series, 
            low_series, 
            acceleration=self.psar_step, 
            maximum=self.psar_max
        )
        self.psar = self.I(lambda: psar_arr, name='PSAR')

        # ADX
        adx_arr = talib.ADX(high_series, low_series, close_series, timeperiod=self.adx_period)
        self.adx = self.I(lambda: adx_arr, name='ADX')

    def next(self):
        if len(self.data) < 2:
            return

        psar_prev = self.psar[-2]
        psar_curr = self.psar[-1]
        price_prev= self.data.Close[-2]
        price_curr= self.data.Close[-1]

        # Flip detection
        flip_bullish = (psar_prev > price_prev) and (psar_curr < price_curr)
        flip_bearish = (psar_prev < price_prev) and (psar_curr > price_curr)

        # ADX checks
        adx_curr = self.adx[-1]
        adx_prev = self.adx[-2]
        adx_rising = adx_curr > adx_prev
        strong_trend = adx_curr > 25

        if not self.position:
            # Long if PSAR flips bullish, ADX>25, ADX rising
            if flip_bullish and strong_trend and adx_rising:
                self.buy()

            # Short if PSAR flips bearish, ADX>25, ADX rising
            elif flip_bearish and strong_trend and adx_rising:
                self.sell()
        else:
            # Exit on PSAR flip
            if (self.position.is_long and flip_bearish) or \
               (self.position.is_short and flip_bullish):
                self.position.close()

data = pd.read_csv(
        r"C:\Users\wille\Desktop\Fevrier 2025\data\ETHUSD-h4-data.csv",  # <-- Chemin vers votre CSV
        parse_dates=['datetime'],
        index_col='datetime'
    )


bt = Backtest(data, PSARADXStrategy, cash=5000, commission=0.002)
stats = bt.run()
print(stats)
bt.plot(resample=False)
