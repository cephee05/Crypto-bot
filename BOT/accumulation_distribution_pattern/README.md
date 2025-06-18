Breakout Strategy on BTC/USD (1h)
This strategy looks for 20-bar breakouts filtered by two volume-based oscillators:

Accumulation/Distribution (A/D): Cumulative A/D must be above its moving average for long entries (below for shorts).

Volume Delta: Net buying volume must be positive for longs (negative for shorts).

Entry Conditions

Long: Price breaks above the prior 20-bar high, A/D > its MA, Volume Delta > 0.

Short: Price breaks below the prior 20-bar low, A/D < its MA, Volume Delta < 0.

Exit & Risk Management

Stop-loss at the opposite 20-bar extreme.

Take-profit set at 2× stop distance.
Actif = BTC/USD
Timeframe = 1h

Backtest sur 150 semaines
![image](https://github.com/user-attachments/assets/d497763a-78b7-42e2-9b2b-54695e1536fb)

Final Equity: $168,910.08

CAGR: 16.08%

Annual Volatility: 20.90%

Sharpe Ratio: 0.77

Sortino Ratio: 1.38

Calmar Ratio: 1.12

Max Drawdown: –14.34%

Profit Factor: 1.54

Win Rate: 44.9%

Expectancy: 1.60% per trade

Kelly Criterion: 0.16

SQN: 1.75

Interpretation: Over three years, the system delivered a solid 16% annualized return with healthy risk-adjusted metrics. The 14% max drawdown is modest, and the >1.3 profit factor signals reliability despite a sub-50% win rate.

MonteCarlos Simulation GRAPH
![image](https://github.com/user-attachments/assets/859b65a2-d7f2-4ced-9c1a-e1b8c9ba6426)
Median Final Capital: $130,259.73

5th Percentile: $89,534.31

95th Percentile: $170,356.46

Probability of Loss: 26.0%

Average Drawdown: –30.6%

Worst Drawdown: –13.5%

Interpretation: Even under random sequencing of trades, there’s a ~74% chance of ending above break-even. Tail risks exist (5% worst ≈ –10.5% to –13.5%), but typical outcomes cluster around the backtested result.

Walk_Forward Equity Curves
![image](https://github.com/user-attachments/assets/83ae23b8-29cf-4dde-960f-19657e751255)
3. Walk-Forward Analysis
Segment	Final Equity	Expectancy	Return	Max DD
1	$107,767.73	1.55%	+7.77%	–4.42%
2	$119,989.39	3.65%	+19.99%	–8.74%
3	$68,913.99	–4.26%	–31.09%	–32.71%
4	$89,597.08	–1.43%	–10.40%	–23.55%
5	$125,557.65	2.54%	+25.56%	–17.01%


Interpretation: Performance is regime-dependent. Segments 1–2 and 5 outperform; segments 3–4 underperform during choppy or trending bear markets. Overall robustness holds, but parameter re-optimization or regime filters could reduce drawdowns in adverse segments.
Key Takeaways
✅ Strengths
Attractive Annual Return (>15% CAGR)

Solid Risk-Adjusted Metrics (Sharpe 0.77, Sortino 1.38, Calmar >1)

Healthy Profit Factor (1.54)

Controlled Max Drawdown (–14.3%)

Reasonable Kelly for position sizing (0.16)

⚠️ Risks & Improvements
Trade Volatility: 26% chance of ending in a loss (Monte Carlo).

Average Drawdown (~–30%) suggests occasional large underwater periods.

Regime Sensitivity: Significant underperformance in certain walk-forward segments.

Win Rate <50% requires strict risk management and psychological resilience.

Possible Enhancements
Regime Filter: Incorporate trend / volatility regimes (e.g., ADX or realized vol) to reduce trades in adverse segments.

Adaptive Parameters: Dynamically adjust lookback or stop distances based on rolling volatility.

Hybrid Signals: Combine with momentum or mean-reversion overlays to smooth returns.

Machine-Learning Filter: Use a simple classifier (e.g., logistic regression) on volume + AD patterns to pre-filter low-probability trades.
