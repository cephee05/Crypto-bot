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

--------------------------------------------------------------------------------------------------BACKTEST
![image](https://github.com/user-attachments/assets/bf7605f5-8ac1-4ac4-9ce2-44b8ebda8b44)
--------------------------------------------------------------------------------------------------
