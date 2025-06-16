def monte_carlo_simulation(data, n=30):
    results = []
    equity_curves = []

    for i in range(n):
        # Resample and shuffle data
        shuffled_data = data.sample(frac=1, replace=True, random_state=np.random.randint(0, 10000))

        # Create and configure the backtest
        bt = Backtest(shuffled_data, LiquidationStrategy, cash=1000000, commission=0.002)

        # Run the backtest
        stats = bt.run()

        # Access the equity curve through the results
        equity_curve = stats['_equity_curve']['Equity']
        equity_curves.append(equity_curve.values)

        final_equity = equity_curve.iloc[-1]
        expectancy = stats['Expectancy'][-1]
        avg_return = stats['Return [%]']
        max_drawdown = stats['Max. Drawdown']

        results.append((final_equity, expectancy, avg_return, max_drawdown))

        print(f"Run {i+1}/{n}: Final Equity = {final_equity:.2f}, Expectancy = {expectancy:.2f}, "
              f"Return = {avg_return:.2f}%, Max Drawdown = {max_drawdown:.2f}%")

    return results, equity_curves


# Perform Monte Carlo simulation
n_simulations = 100
results, equity_curves = monte_carlo_simulation(data, n_simulations)

# Plot results
plt.figure(figsize=(12, 6))

for equity_curve in equity_curves:
    plt.plot(equity_curve, color='blue', alpha=0.1)

plt.title(f"Monte Carlo Simulation ({n_simulations} runs)")
plt.xlabel('Time')
plt.ylabel('Equity')
plt.show()
