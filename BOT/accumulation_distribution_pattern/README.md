Cette stratégie cherche des cassures sur une période de 20 bougies en surveillant l'AccumulationDistribution cumulée et le Volume Delta
on achète si le prix dépasse le plus haut précédent lorsque l'AD est au-dessus de sa moyenne et que le Volume Delta est positif on vend 
si le prix casse le plus bas précédent avec un AD sous sa moyenne et un Volume Delta négatif chaque position est protégée par un stoploss 
sur l'extrême inverse et un takeprofit fixé au double de la distance du stop

'''
Backtest
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




