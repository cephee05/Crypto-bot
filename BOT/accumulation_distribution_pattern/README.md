Cette stratégie cherche des cassures sur une période de 20 bougies en surveillant l'AccumulationDistribution cumulée et le Volume Delta
on achète si le prix dépasse le plus haut précédent lorsque l'AD est au-dessus de sa moyenne et que le Volume Delta est positif on vend 
si le prix casse le plus bas précédent avec un AD sous sa moyenne et un Volume Delta négatif chaque position est protégée par un stoploss 
sur l'extrême inverse et un takeprofit fixé au double de la distance du stop

actif = BTC/USD
Timeframe = 1h

Backtest sur 150 semaines
![image](https://github.com/user-attachments/assets/d497763a-78b7-42e2-9b2b-54695e1536fb)



MonteCarlos Simulation GRAPH
![image](https://github.com/user-attachments/assets/859b65a2-d7f2-4ced-9c1a-e1b8c9ba6426)
Moyenne du capital final: 127931.69
Médiane du capital final: 130259.73
Quantile 5%: 89534.31
Quantile 95%: 170356.46
Probabilité de perte: 26.00%
Drawdown moyen: -30.55%
Max Drawdown observé: -13.46%

Walk_Forward Equity Curves
![image](https://github.com/user-attachments/assets/83ae23b8-29cf-4dde-960f-19657e751255)
Walk-Forward Results:
Segment 1: Final Equity=107767.73, Expectancy=1.55%, Return=7.77%, MaxDD=-4.42%   
Segment 2: Final Equity=119989.39, Expectancy=3.65%, Return=19.99%, MaxDD=-8.74%  
Segment 3: Final Equity=68913.99, Expectancy=-4.26%, Return=-31.09%, MaxDD=-32.71%
Segment 4: Final Equity=89597.08, Expectancy=-1.43%, Return=-10.40%, MaxDD=-23.55%
Segment 5: Final Equity=125557.65, Expectancy=2.54%, Return=25.56%, MaxDD=-17.01% 

ANALYSE 
Equity Final	$168,910.08	Performance très correcte
CAGR	16.08%	Excellent taux composé sur 3 ans
Annual Return	16.06%	Aligné avec le CAGR, pas trop volatile
Volatility (Ann.)	20.90%	Volatilité modérée
Sharpe Ratio	0.77	Correct, mais améliorable
Sortino Ratio	1.38	Bon, moins pénalisé par les drawdowns
Calmar Ratio	1.12	👍 Supérieur à 1 : acceptable
Max. Drawdown	-14.34%	Plutôt sain, si stable
Profit Factor	1.54	Très bon (au-delà de 1.3, c’est fiable)
Win Rate	44.90%	Moins de 50%, mais compensé par expectancy
Expectancy	1.60%	Positif : chaque trade rapporte en moyenne 1.6%
Kelly Criterion	0.16	Faible mais exploitable
SQN	1.75	Bon système (entre 1.6 et 2.0 = acceptable à bon)

📌 Conclusion synthétique
✅ Points forts :

Bon rendement annuel (>15%)
Bon Calmar et Sortino
Bon profit factor
Bonne gestion du risque moyen

⚠️ Points à surveiller :

Volatilité du système (surtout segment 3)
26% de probabilité de finir en perte (à minimiser)
Drawdown moyen élevé (-30% !), à confirmer/optimiser
