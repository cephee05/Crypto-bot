# Function to perform Walk-Forward Optimization
def walk_forward_optimization(data, strategy, initial_cash=100000, commission=0.002, train_percent=0.7, test_percent=0.3):
    n = len(data)
    train_size = int(n * train_percent)
    test_size = int(n * test_percent)
    results = []
    equity_curves = []

    start = 0
    while start + train_size + test_size <= n:
        train_data = data.loc[start:start + train_size]
        test_data = data.loc[start + train_size:start + train_size + test_size]

        bt_train = Backtest(train_data, strategy, cash=initial_cash, commission=commission)
        stats_train = bt_train.run()

        # Apply the strategy with optimized parameters on the test data
        bt_test = Backtest(test_data, strategy, cash=initial_cash, commission=commission)
        stats = bt_test.run()

        equity_curve = stats['_equity_curve']['Equity']
        equity_curves.append(equity_curve.values)

        final_equity = equity_curve.iloc[-1]
        expectancy = stats['Expectancy'][-1]
        avg_return = stats['Return [%]']
        max_drawdown = stats['Max. Drawdown [%]']

        results.append((final_equity, expectancy, avg_return, max_drawdown))

        start += test_size

    return results, equity_curves
