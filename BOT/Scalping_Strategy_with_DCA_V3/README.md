Source: https://www.tradingview.com/script/R1WjVRPU-Scalping-Strategy-with-DCA-V3/

Voici la stratégie en résumé :

- **Tendance & Confirmation multi-indicateurs**  
  1. Filtre principal : prix au-dessus (long) ou en-dessous (short) de l’EMA 48 puis RSI 14 (>20/​<80) et croisement MACD (12/26/9).  
  2. Renfort : détection de divergence RSI, touches extrêmes des bandes de Bollinger, et validation du même signal sur le graphique journalier.

- **Mécanisme DCA 1-2-6**  
  1. Entrée initiale : 1 unité.  
  2. Si le prix baisse de 1 %, achat de 2 unités.  
  3. Si le prix baisse de 2 %, achat de 6 unités et ajustement du stop-loss à 1,3 %.

- **Gestion des profits et des pertes**  
  - **TP1** : +0,5 % → clôt 25 % de la position.  
  - **TP2** : +1 % → clôt 50 % de la position et place le stop-loss au point d’entrée.  
  - **SL initial** : –1,5 % du prix moyen d’entrée (trailing stop après DCA complet).

Cette approche combine robustesse (EMA/RSI/MACD), opportunités de retournement (divergences + Bollinger) et gestion de risque dynamique via DCA et sorties par paliers.

--------------------------------------------------------------------------------------------------
BACKTEST
![image](https://github.com/user-attachments/assets/bf7605f5-8ac1-4ac4-9ce2-44b8ebda8b44)
--------------------------------------------------------------------------------------------------
Distribution du Capital Final
![image](https://github.com/user-attachments/assets/51fbfe98-d55f-4917-a871-35ad94734cde)
Monte Carlo Equity Curves
![image](https://github.com/user-attachments/assets/f16d8c33-27e1-468b-b0bc-5d355fecb4bb)
Moyenne du capital final: 448990.29
Médiane du capital final: 446980.38
Quantile 5%: 369967.23
Quantile 95%: 527195.46
Drawdown moyen: -17.98%
Max Drawdown observé: -12.24%
Moyenne final equity: 448990.29
Probabilité de perte: 0.00%
--------------------------------------------------------------------------------------------------
=== Walk-Forward ===
Seg 1: Equity=141599.64, Expectancy=1.35%, Ret=28.73%, MaxDD=-5.39%
Seg 2: Equity=141543.09, Expectancy=1.20%, Ret=28.68%, MaxDD=-6.76%
Seg 3: Equity=110086.74, Expectancy=0.40%, Ret=0.08%, MaxDD=-9.94%
Seg 4: Equity=128868.40, Expectancy=0.75%, Ret=17.15%, MaxDD=-5.08%
Seg 5: Equity=108923.85, Expectancy=0.39%, Ret=-0.98%, MaxDD=-14.33%
