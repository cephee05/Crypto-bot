Scalping Strategy with DCA (v3)
Source: TradingView Script R1WjVRPU

Asset: BTC/USD
Timeframe: 1 h

Signal Logic
Trend filter: Price above (long) or below (short) the 48-period EMA

Confirmation:

RSI 14 crosses over 20 (long) or under 80 (short)

MACD (12, 26, 9) line/ signal crossover in direction of trade

Strengtheners:

RSI divergence on entry timeframe

Price touching Bollinger Bands extremes

Same signal confirmed on daily chart

DCA & Risk Management
Initial entry: 1 unit

DCA #1: If price drops –1 %, buy 2 units

DCA #2: If price drops –2 % further, buy 6 units; tighten SL to –1.3 % from avg price

Stop-Loss: –1.5 % from avg entry (trailing after full DCA)

Take-Profit:

TP1 @ +0.5 % → close 25 % of position

TP2 @ +1 % → close 50 % of remaining & move SL to breakeven


--------------------------------------------------------------------------------------------------

=== BACKTEST ===
![image](https://github.com/user-attachments/assets/bf7605f5-8ac1-4ac4-9ce2-44b8ebda8b44)
--------------------------------------------------------------------------------------------------

=== Distribution du Capital Final ===
![image](https://github.com/user-attachments/assets/51fbfe98-d55f-4917-a871-35ad94734cde)

=== Monte Carlo Equity Curves ===
![image](https://github.com/user-attachments/assets/f16d8c33-27e1-468b-b0bc-5d355fecb4bb)
| Statistic               | Value       |
|------------------------:|------------:|
| Mean Final Capital      | \$127,931.69 |
| Median Final Capital    | \$130,259.73 |
| 5% Quantile             | \$89,534.31  |
| 95% Quantile            | \$170,356.46 |
| Probability of Loss     | 26.00%       |
| Mean Drawdown           | −30.55%      |
| Max Drawdown Observed   | −13.46%      |

--------------------------------------------------------------------------------------------------
=== Walk-Forward ===
![image](https://github.com/user-attachments/assets/3422a792-722b-454e-a135-db5443167a66)
| Segment | Final Equity | Expectancy | Return   | Max Drawdown |
|-------:|--------------:|-----------:|---------:|-------------:|
| 1      | \$107,767.73  |   1.55%    |  +7.77%  |    −4.42%    |
| 2      | \$119,989.39  |   3.65%    | +19.99%  |    −8.74%    |
| 3      | \$68,913.99   |  −4.26%    | −31.09%  |   −32.71%    |
| 4      | \$89,597.08   |  −1.43%    | −10.40%  |   −23.55%    |
| 5      | \$125,557.65  |   2.54%    | +25.56%  |   −17.01%    |
-------------------------------------------------------------------------------------------------
Overall Analysis
Annualized Return: ~ 16 % CAGR

Volatility (ann.): ~ 21 %

Sharpe Ratio: 0.77

Sortino Ratio: 1.38

Calmar Ratio: 1.12

Max Drawdown: −14.3 %

Profit Factor: 1.54

Win Rate: 44.9 %

Expectancy per Trade: +1.6 %

Kelly Criterion: 0.16

SQN: 1.75

🔑 Strengths
Robust trend-filter + multi-indicator confirmation

Controlled downside via DCA & dynamic SL

Good risk-adjusted returns (Sharpe > 0.7, Calmar > 1)

⚠️ Risks & Points to Monitor
Drawdowns can reach ~ −17 % average in Monte Carlo

Segment-level variability (especially seg 3)

Zero probability of full-period loss—may decline in true live market


