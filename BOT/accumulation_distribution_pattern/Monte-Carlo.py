'''
Moyenne du capital final: 127931.69
Médiane du capital final: 130259.73
Quantile 5%: 89534.31
Quantile 95%: 170356.46
Probabilité de perte: 26.00%
Drawdown moyen: -30.55%
Max Drawdown observé: -13.46%
'''


import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
import matplotlib.pyplot as plt

class AccumDistVolumeDeltaStrategy(Strategy):
    period = 20

    def init(self):
        high, low, close, open_, volume = map(pd.Series, [
            self.data.High, self.data.Low, self.data.Close, self.data.Open, self.data.Volume
        ])

        mfm = ((close - low) - (high - close)) / np.maximum((high - low), 1e-6)
        ad = (mfm * volume).cumsum()

        self.ad = ad.to_numpy()
        self.ad_sma = ad.rolling(self.period).mean().to_numpy()
        self.volDelta = np.where(close > open_, volume, np.where(close < open_, -volume, 0))
        self.hh = high.rolling(self.period).max().to_numpy()
        self.ll = low.rolling(self.period).min().to_numpy()

    def next(self):
        i = len(self.data.Close) - 1
        if i < self.period:
            return

        close_price = self.data.Close[i]

        if not self.position:
            if close_price > self.hh[i-1] and self.ad[i] > self.ad_sma[i] and self.volDelta[i] > 0:
                risk = max(close_price - self.ll[i-1], 0.001)
                tp = close_price + 2 * risk
                self.buy(sl=self.ll[i-1], tp=tp, size=1)

            elif close_price < self.ll[i-1] and self.ad[i] < self.ad_sma[i] and self.volDelta[i] < 0:
                risk = max(self.hh[i-1] - close_price, 0.001)
                tp = close_price - 2 * risk
                self.sell(sl=self.hh[i-1], tp=tp, size=1)

data = pd.read_csv(r"C:\Users\wille\Desktop\Fevrier 2025\BTCUSD-1h-150wks-data.csv", 
                   parse_dates=['datetime'], index_col='datetime')

def monte_carlo_simulation(data, n=100):
    results = []
    equity_curves = []

    for _ in range(n):
        shuffled_data = data.sample(frac=1, replace=True)
        bt = Backtest(shuffled_data, AccumDistVolumeDeltaStrategy, cash=110000, commission=0.002)
        stats = bt.run()

        equity_curve = stats['_equity_curve']['Equity'].values
        equity_curves.append(equity_curve)

        results.append({
            'final_equity': equity_curve[-1],
            'expectancy': stats['Expectancy [%]'],
            'return_pct': stats['Return [%]'],
            'max_drawdown': stats['Max. Drawdown [%]']
        })

    return pd.DataFrame(results), equity_curves

results_df, equity_curves = monte_carlo_simulation(data)

# Analyse statistique
final_equities = results_df['final_equity']
mean_eq, median_eq = final_equities.mean(), final_equities.median()
quantile_5, quantile_95 = final_equities.quantile(0.05), final_equities.quantile(0.95)
prob_loss = np.mean(final_equities < 110000)
mean_dd, max_dd = results_df['max_drawdown'].mean(), results_df['max_drawdown'].max()

print(f"Moyenne du capital final: {mean_eq:.2f}")
print(f"Médiane du capital final: {median_eq:.2f}")
print(f"Quantile 5%: {quantile_5:.2f}")
print(f"Quantile 95%: {quantile_95:.2f}")
print(f"Probabilité de perte: {prob_loss*100:.2f}%")
print(f"Drawdown moyen: {mean_dd:.2f}%")
print(f"Max Drawdown observé: {max_dd:.2f}%")

# Visualisation des résultats
plt.figure(figsize=(12, 6))
for equity_curve in equity_curves:
    plt.plot(equity_curve, color='blue', alpha=0.05)

plt.title("Monte Carlo Simulation (Equity Curves)")
plt.xlabel('Temps')
plt.ylabel('Équité')
plt.grid(alpha=0.3)
plt.show()

# Histogramme des résultats finaux
plt.figure(figsize=(12, 6))
plt.hist(final_equities, bins=20, edgecolor='black', color='skyblue')
plt.axvline(mean_eq, color='red', linestyle='--', label=f'Moyenne: {mean_eq:.2f}')
plt.axvline(median_eq, color='green', linestyle='--', label=f'Médiane: {median_eq:.2f}')
plt.xlabel('Capital Final')
plt.ylabel('Fréquence')
plt.title('Distribution du Capital Final (Monte Carlo)')
plt.legend()
plt.show()
