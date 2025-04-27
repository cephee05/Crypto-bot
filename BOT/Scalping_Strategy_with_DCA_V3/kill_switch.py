## Kill-Switch Automatique

Pour protéger le capital et suspendre la stratégie en cas de conditions défavorables, implémentez ces règles :

1. **Drawdown Maximal > 20 %**  
   - Si l’équité en temps réel chute de plus de 20 % par rapport à son dernier pic, **stopper immédiatement** toutes les prises de position.

2. **Perte Cumulée > 5 % sur 7 Jours**  
   - Si le PnL net glissant sur 7 jours descend sous – 5 %, **mettre en pause** la stratégie pendant 48 h pour révision.

3. **Expectancy Walk-Forward < 0,5 %**  
   - Si, lors d’un segment de test Walk-Forward, l’“Expectancy [%]” est inférieure à 0,5 %, **arrêter** l’exécution et ré-optimiser les paramètres.

4. **Sortie de l’Intervalle Monte Carlo [5 %; 95 %]**  
   - Si le capital en réel sort du quantile 5 %–95 % de la distribution Monte Carlo (p.ex. < Q5 ou > Q95), **suspendre** pour diagnostic.

5. **Volatilité Annuelle > 80 %**  
   - En cas de volatilité annualisée du sous-jacent > 80 %, **désactiver** la stratégie jusqu’à retour sous ce seuil.

6. **Fenêtre d’Événements Majeurs**  
   - Avant et après annonces ou événements critiques (halving, forks, publications macro), **désactiver** la stratégie de – 1 h à + 2 h.
