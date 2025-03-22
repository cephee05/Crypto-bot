Cette stratégie cherche des cassures sur une période de 20 bougies en surveillant l'AccumulationDistribution cumulée et le Volume Delta
on achète si le prix dépasse le plus haut précédent lorsque l'AD est au-dessus de sa moyenne et que le Volume Delta est positif on vend 
si le prix casse le plus bas précédent avec un AD sous sa moyenne et un Volume Delta négatif chaque position est protégée par un stoploss 
sur l'extrême inverse et un takeprofit fixé au double de la distance du stop

Backtest
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
