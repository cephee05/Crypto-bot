import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_index()
    # EMA48
    df['EMA48'] = EMAIndicator(df['Close'], window=48).ema_indicator()
    # RSI14
    df['RSI'] = RSIIndicator(df['Close'], window=14).rsi()
    # MACD
    macd = MACD(df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['MACD']        = macd.macd()
    df['MACD_SIGNAL'] = macd.macd_signal()
    # Bollinger Bands 20,2
    df['BB_MID']   = df['Close'].rolling(20).mean()
    std = df['Close'].rolling(20).std()
    df['BB_UPPER'] = df['BB_MID'] + 2 * std
    df['BB_LOWER'] = df['BB_MID'] - 2 * std
    # RSI divergences
    dclose = df['Close'].diff()
    drsi   = df['RSI'].diff()
    df['RSI_DIV_BULL'] = (dclose < 0) & (drsi > 0)
    df['RSI_DIV_BEAR'] = (dclose > 0) & (drsi < 0)
    # Confirmation daily
    daily = df.resample('D').agg({'EMA48':'last','RSI':'last'})
    df['D_EMA48'] = daily['EMA48'].reindex(df.index, method='ffill')
    df['D_RSI']   = daily['RSI'].reindex(df.index, method='ffill')
    return df.dropna()

class MultiIndicatorDCA(Strategy):
    TP1    = 0.005
    TP2    = 0.01
    SL0    = 0.015
    SL_ADJ = 0.013
    DCA1   = 0.01
    DCA2   = 0.02

    def init(self):
        self.entry_price  = None
        self.current_size = 0
        self.is_long      = None

    def next(self):
        price    = self.data.Close[-1]
        ema48    = self.data.EMA48[-1]
        rsi      = self.data.RSI[-1]
        macd     = self.data.MACD[-1]
        sig      = self.data.MACD_SIGNAL[-1]
        bb_low   = self.data.BB_LOWER[-1]
        bb_high  = self.data.BB_UPPER[-1]
        div_bull = self.data.RSI_DIV_BULL[-1]
        div_bear = self.data.RSI_DIV_BEAR[-1]
        d_ema48  = self.data.D_EMA48[-1]
        d_rsi    = self.data.D_RSI[-1]

        # Conditions d'entrée
        cond_long    = (price > ema48 and rsi > 20 and macd > sig
                        and d_ema48 > price and d_rsi > 50)
        cond_bb_long = price < bb_low and rsi < 20
        cond_div_long= div_bull
        cond_short   = (price < ema48 and rsi < 80 and macd < sig
                        and d_ema48 < price and d_rsi < 50)
        cond_bb_short= price > bb_high and rsi > 80
        cond_div_short= div_bear

        # Nouvelle position
        if self.current_size == 0:
            if cond_long or cond_bb_long or cond_div_long:
                self.buy(size=1)
                self.entry_price  = price
                self.current_size = 1
                self.is_long      = True
            elif cond_short or cond_bb_short or cond_div_short:
                self.sell(size=1)
                self.entry_price  = price
                self.current_size = 1
                self.is_long      = False
            return

        # Calcul PnL %
        pnl = ((price - self.entry_price) / self.entry_price
               if self.is_long else
               (self.entry_price - price) / self.entry_price)

        # DCA 1-2-6
        if pnl <= -self.DCA1 and self.current_size == 1:
            self.buy(size=2)
            self.entry_price  = (self.entry_price + 2 * price) / 3
            self.current_size = 3
        if pnl <= -self.DCA2 and self.current_size == 3:
            self.buy(size=6)
            self.entry_price  = (3*self.entry_price + 6*price) / 9
            self.current_size = 9
            # Ajust SL
            sl = (self.entry_price * (1-self.SL_ADJ)
                  if self.is_long else
                  self.entry_price * (1+self.SL_ADJ))
            self.position.sl = sl

        # TP partiels
        if pnl >= self.TP1 and self.current_size > 0:
            qty = max(1, int(0.25*self.current_size))
            if self.is_long: self.sell(size=qty)
            else:             self.buy(size=qty)
            self.current_size -= qty

        # 2ᵉ TP + breakeven
        if pnl >= self.TP2 and self.current_size > 0:
            qty = max(1, int(0.50*self.current_size))
            if self.is_long: self.sell(size=qty)
            else:             self.buy(size=qty)
            self.current_size -= qty
            self.position.sl = self.entry_price

        # SL initial
        if pnl <= -self.SL0:
            self.position.close()
            self.current_size = 0

def monte_carlo_simulation(data: pd.DataFrame, n: int = 100):
    results, curves = [], []
    for _ in range(n):
        sample = data.sample(frac=1, replace=True).sort_index()
        bt     = Backtest(sample, MultiIndicatorDCA,
                          cash=110000, commission=0.00075,
                          trade_on_close=True)
        stats  = bt.run()
        eq     = stats['_equity_curve']['Equity'].values
        curves.append(eq)
        results.append({
            'final_equity': eq[-1],
            'expectancy':   stats['Expectancy [%]'],
            'return_pct':   stats['Return [%]'],
            'max_dd':       stats['Max. Drawdown [%]']
        })
    return pd.DataFrame(results), curves

def walk_forward_optimization(data: pd.DataFrame, strategy, cash, commission, train_pct, test_pct):
    n          = len(data)
    train_size = int(n * train_pct)
    test_size  = int(n * test_pct)
    results, curves = [], []
    start = 0
    while start + train_size + test_size <= n:
        train = data.iloc[start:start+train_size]
        test  = data.iloc[start+train_size:start+train_size+test_size]
        # backtest train (optionnel d’ajuster ici les hyperparams)
        Backtest(train, strategy, cash=cash, commission=commission).run()
        bt   = Backtest(test, strategy, cash=cash, commission=commission)
        stats= bt.run()
        eq   = stats['_equity_curve']['Equity'].values
        curves.append(eq)
        results.append({
            'final_equity': eq[-1],
            'expectancy':   stats['Expectancy [%]'],
            'return_pct':   stats['Return [%]'],
            'max_dd':       stats['Max. Drawdown [%]']
        })
        start += test_size
    return pd.DataFrame(results), curves

if __name__ == "__main__":
    # 1) Lecture + préparation
    df_raw = pd.read_csv(
        r"C:\Users\wille\Desktop\DATA\crypto_data\stock_data\BTCUSD-1h-150wks-data.csv",
        parse_dates=['datetime'], index_col='datetime'
    )
    data   = prepare_data(df_raw)

    # 2) Backtest simple
    bt = Backtest(data, MultiIndicatorDCA,
                  cash=110000, commission=0.00075,
                  trade_on_close=True)
    stats = bt.run()
    print("=== Backtest simple ===")
    print(stats)
    bt.plot(resample='4h')
res_wf, curves_wf = walk_forward_optimization(
        data, MultiIndicatorDCA,
        cash=110000, commission=0.002,
        train_pct=0.45, test_pct=0.10
    )
    print("=== Walk-Forward ===")
    for i, row in res_wf.iterrows():
        print(f"Seg {i+1}: Equity={row.final_equity:.2f}, "
              f"Expectancy={row.expectancy:.2f}%, "
              f"Ret={row.return_pct:.2f}%, "
              f"MaxDD={row.max_dd:.2f}%")

    # Affichage des courbes
    plt.figure(figsize=(10,5))
    for c in curves_mc:
        plt.plot(c, alpha=0.05, color='blue')
    plt.title("Monte Carlo Equity Curves")
    plt.show()

    plt.figure(figsize=(10,5))
    for c in curves_wf:
        plt.plot(c, alpha=0.5)
    plt.title("Walk-Forward Equity Curves")
    plt.show()
