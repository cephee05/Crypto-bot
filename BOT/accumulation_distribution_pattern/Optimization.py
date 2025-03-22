'''
Paramètres optimisés :
period = 21
target_rr = 2
'''
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

class AccumDistVolumeDeltaStrategy(Strategy):
    period = 20      # Période de lookback (valeur par défaut)
    target_rr = 2    # Ratio risque/gain par défaut (TP = entry ± target_rr * risk)

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
        # Indice de la bougie actuelle
        i = len(self.data.Close) - 1

        # S'assurer d'avoir suffisamment de données
        if i < self.period:
            return

        current_close = self.data.Close[i]

        if not self.position:
            # Condition pour une entrée LONG :
            # - Le prix casse le plus haut de la bougie précédente
            # - L'AD est au-dessus de sa SMA
            # - Le Volume Delta est positif
            if (current_close > self.hh[i-1] and
                self.ad[i] > self.ad_sma[i] and
                self.volDelta[i] > 0):
                
                risk = current_close - self.ll[i-1]
                if risk <= 0:
                    risk = 0.001  # éviter un risque nul
                tp = current_close + self.target_rr * risk  # TP en fonction du ratio risque/gain

                self.buy(sl=self.ll[i-1], tp=tp, size=1)

            # Condition pour une entrée SHORT :
            # - Le prix casse le plus bas de la bougie précédente
            # - L'AD est en dessous de sa SMA
            # - Le Volume Delta est négatif
            elif (current_close < self.ll[i-1] and
                  self.ad[i] < self.ad_sma[i] and
                  self.volDelta[i] < 0):

                risk = self.hh[i-1] - current_close
                if risk <= 0:
                    risk = 0.001
                tp = current_close - self.target_rr * risk

                self.sell(sl=self.hh[i-1], tp=tp, size=1)

if __name__ == '__main__':
    # Lecture de la dataframe
    data = pd.read_csv(
        r"C:\Users\wille\Desktop\Fevrier 2025\data\BTCUSD-h4-data.csv",
        parse_dates=['datetime'],
        index_col='datetime'
    )

    bt = Backtest(data, AccumDistVolumeDeltaStrategy, cash=110000, commission=0.002)

    # Optimisation de la stratégie : on optimise la période et le ratio risque/gain
    # Ici, on teste des périodes entre 15 et 30 et des ratios risque/gain de 1.5, 2, 2.5 et 3.
    stats = bt.optimize(
        period=range(11, 30),
        target_rr=[2, 3, 4, 5, 8, 13],
        maximize='Equity Final [$]',  # Objectif d'optimisation
        constraint=lambda param: param.period > 0  # Contrainte minimale (facultative)
    )

    print(stats)
    bt.plot()
    print("Paramètres optimisés :")
    print("period =", stats._strategy.period)
    print("target_rr =", stats._strategy.target_rr)
