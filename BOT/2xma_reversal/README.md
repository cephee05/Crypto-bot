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


=================================================================================================================
Monte Carlo Equity Cruves (50runs)
![image](https://github.com/user-attachments/assets/fc6413f4-6463-438a-8f00-5573d4aa5733)
