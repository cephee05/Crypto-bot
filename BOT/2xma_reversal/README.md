🎯 Vue d’ensemble
MA Reversal Strategy est une stratégie de retournement multi-timeframe basée sur deux moyennes mobiles simples (SMA), conçue pour capter les phases de repli et de rebond d’un actif de manière systématique. Elle fonctionne sur n’importe quelle granularité (5 min, 15 min, 1 h, daily…) dès lors que vous fournissez un DataFrame OHLCV indexé en datetime.

📊 Concept de la stratégie
Repérage des zones de “range” :

Lorsque le prix évolue entre une SMA rapide et une SMA lente, on anticipe un retour vers le bas de la bande (short).

Lorsque le prix déclenche une cassure haussière au-dessus des deux SMA, on entre long pour profiter du momentum.

Gestion systématique du risque :

À chaque entrée, on place immédiatement un stop-loss et un take-profit en pourcentage du prix d’entrée.

Pas de pyramiding ; une seule position à la fois (exclusion d’ordres multiples).

Fermeture anticipée :

En position short, si le prix franchit la SMA lente à la hausse, on clôture pour éviter un retournement complet.

====================================================================
Backtest // BTC 5 min // 100 weeks
![image](https://github.com/user-attachments/assets/fa1a3af9-75df-427d-b887-6afa6db63713)
Start                     2023-06-05 16:45:00
End                       2025-05-05 16:35:00
Duration                    699 days 23:50:00
Exposure Time [%]                    97.99679
Equity Final [$]                 148162.31183
Equity Peak [$]                  172516.31143
Commissions [$]                   19473.12097
Return [%]                           34.69301
Buy & Hold Return [%]               267.10686
Return (Ann.) [%]                    16.89179
Volatility (Ann.) [%]                27.98477
CAGR [%]                             16.80055
Sharpe Ratio                          0.60361
Sortino Ratio                         1.04695
Calmar Ratio                          0.69123
Max. Drawdown [%]                   -24.43714
Avg. Drawdown [%]                    -0.70008
Max. Drawdown Duration      242 days 09:00:00
Avg. Drawdown Duration        2 days 14:51:00
# Trades                                   79
Win Rate [%]                         54.43038
Best Trade [%]                       10.08658
Worst Trade [%]                     -10.00791
Avg. Trade [%]                        1.41626
Max. Trade Duration          54 days 23:40:00
Profit Factor                         1.66712
Expectancy [%]                         1.7446
SQN                                   1.19934
Kelly Criterion                       0.15721
_strategy                  MAReversalStrategy
_equity_curve                             ...
_trades                       Size  EntryB...
dtype: object

====================================================================
Monte Carlo Equity Cruves (50runs)
![image](https://github.com/user-attachments/assets/fc6413f4-6463-438a-8f00-5573d4aa5733)
