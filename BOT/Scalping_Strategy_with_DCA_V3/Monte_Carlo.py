
# -*- coding: utf-8 -*-
"""
Backtest de la stratégie avancée Multi-Indicator + DCA 1-2-6

Composants :
- EMA 48 (trend)
- RSI 14 (momentum + divergence)
- MACD (12,26,9)
- Bollinger Bands (20,2)
- Confirmation multi-timeframe (H1 + Daily)

Mécanisme DCA : 1 – 2 – 6 units
TP tiers : 25% à TP1 (0.5%), 50% à TP2 (1%), reste avec TS
SL dynamique :
  • Initial SL = 1.5% du prix moyen d’entrée
  • Après DCA full, SL ajusté à 1.3%
  • Breakeven après TP2


"""
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_index()
    # EMA 48
    df['EMA48'] = EMAIndicator(df['Close'], window=48).ema_indicator()
    # RSI 14
    df['RSI']   = RSIIndicator(df['Close'], window=14).rsi()
    # MACD
    macd = MACD(df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['MACD']        = macd.macd()
    df['MACD_SIGNAL'] = macd.macd_signal()
    # Bollinger Bands 20,2
    mid = df['Close'].rolling(20).mean()
    std = df['Close'].rolling(20).std()
    df['BB_UPPER'] = mid + 2 * std
    df['BB_LOWER'] = mid - 2 * std
    df['BB_MID']   = mid
    # RSI divergence
    df['RSI_DIV_BULL'] = (df['Close'].diff() < 0) & (df['RSI'].diff() > 0)
    df['RSI_DIV_BEAR'] = (df['Close'].diff() > 0) & (df['RSI'].diff() < 0)
    # Multi-timeframe : daily EMA48 & RSI (ffill)
    daily = df.resample('D').agg({'EMA48':'last','RSI':'last'})
    df['D_EMA48'] = daily['EMA48'].reindex(df.index, method='ffill')
    df['D_RSI']   = daily['RSI'].reindex(df.index, method='ffill')
    return df.dropna()

class MultiIndicatorDCA(Strategy):
    TP1 = 0.005
    TP2 = 0.01
    SL0 = 0.015
    SL_ADJ = 0.013
    DCA1 = 0.01
    DCA2 = 0.02

    def init(self):
        # Variables de suivi de la position
        self.entry_price = None
        self.current_size = 0
        self.is_long = None

    def next(self):
        price = self.data.Close[-1]
        ema48 = self.data.EMA48[-1]
        rsi   = self.data.RSI[-1]
        macd  = self.data.MACD[-1]
        sig   = self.data.MACD_SIGNAL[-1]
        bb_lower = self.data.BB_LOWER[-1]
        bb_upper = self.data.BB_UPPER[-1]
        div_bull = self.data.RSI_DIV_BULL[-1]
        div_bear = self.data.RSI_DIV_BEAR[-1]
        d_ema48  = self.data.D_EMA48[-1]
        d_rsi    = self.data.D_RSI[-1]

        # Conditions d'entrée
        cond_long = price > ema48 and rsi > 20 and macd > sig and d_ema48 > price and d_rsi > 50
        cond_bb_long = price < bb_lower and rsi < 20
        cond_div_long = div_bull
        cond_short = price < ema48 and rsi < 80 and macd < sig and d_ema48 < price and d_rsi < 50
        cond_bb_short = price > bb_upper and rsi > 80
        cond_div_short = div_bear

        # Nouvelle position
        if self.current_size == 0:
            if cond_long or cond_bb_long or cond_div_long:
                self.buy(size=1)
                self.entry_price = price
                self.current_size = 1
                self.is_long = True
            elif cond_short or cond_bb_short or cond_div_short:
                self.sell(size=1)
                self.entry_price = price
                self.current_size = 1
                self.is_long = False
            return

        # Calcul du PnL en %
        pnl = (price - self.entry_price) / self.entry_price if self.is_long else (self.entry_price - price) / self.entry_price

        # DCA
        if pnl <= -self.DCA1 and self.current_size == 1:
            self.buy(size=2)
            self.entry_price = (self.entry_price + 2 * price) / 3
            self.current_size = 3
        if pnl <= -self.DCA2 and self.current_size == 3:
            self.buy(size=6)
            self.entry_price = (3 * self.entry_price + 6 * price) / 9
            self.current_size = 9
            # ajuster SL après DCA complet
            sl = self.entry_price * (1 - self.SL_ADJ) if self.is_long else self.entry_price * (1 + self.SL_ADJ)
            self.position.sl = sl

        # Take Profit partiel
        if pnl >= self.TP1 and self.current_size > 0:
            qty = max(int(0.25 * self.current_size), 1)
            if self.is_long:
                self.sell(size=qty)
            else:
                self.buy(size=qty)
            self.current_size -= qty

        if pnl >= self.TP2 and self.current_size > 0:
            qty = max(int(0.50 * self.current_size), 1)
            if self.is_long:
                self.sell(size=qty)
            else:
                self.buy(size=qty)
            self.current_size -= qty
            # breakeven SL
            self.position.sl = self.entry_price

        # Stop Loss
        if pnl <= -self.SL0:
            self.position.close()
            self.current_size = 0
if __name__ == "__main__":
    # Charger vos données BTCUSDT_1H.csv (DateTimeIndex, colonnes : Open,High,Low,Close,Volume)
    data = pd.read_csv(r"C:\Users\wille\Desktop\DATA\crypto_data\stock_data\BTCUSD-1h-150wks-data.csv", index_col=0, parse_dates=True)
    data = prepare_data(data)

    bt = Backtest(
        data,
        MultiIndicatorDCA,
        cash=110000,
        commission=0.002,
        trade_on_close=True
    )

    stats = bt.run()
    print(stats)
    bt.plot()
