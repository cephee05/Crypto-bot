# Crypto-bot

I regularly develop various trading bots (scripts, automations, optimizations) and share the most relevant ones here.


* **crypto-bot/** (racine du projet)

  * **bots/**

    * Chaque stratégie dans son propre dossier

      * `config.py`
      * `strategy.py`
      * `backtest.py`
      * `README.md`
  * **data/**

    * **raw/** : CSV bruts (OHLC 1m)
    * **processed/** : CSV de features générés par `src/train.py`
  * **backtest/** :

    * Scripts ou notebooks pour Monte Carlo, Walk-Forward, analyses avancées
  * **requirements.txt** :

    * Dépendances Python
  * **README.md** :

    * Présentation, installation, usage et “Backtest Tips”



⚠️ **Disclaimer:**  
The trading strategies shared on this GitHub repository are for educational purposes only. They do not guarantee profits and carry the risk of financial loss. Before using or investing, make sure you fully understand how they work, conduct your own tests, and only commit funds you can afford to lose.
