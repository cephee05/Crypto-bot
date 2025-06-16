class DelayedLiquidationStrategy(LiquidationStrategy):
    delay_minutes = 0  # No delay by default

    def next(self):
        # If there is a trade start index, check the delay
        if self.trade_start_idx is not None:
            # Calculate how many bars have passed since the trade signal
            bars_since_trade_start = len(self.data.Close) - self.trade_start_idx
            if bars_since_trade_start < self.delay_minutes:
                return  # Skip execution if the delay period has not passed

        # Execute the base strategy logic
        super().next()

#####################################################################
# Ensure the DataFrame is sorted by the index
data.sort_index(inplace=True)

def run_alpha_decay_test(data, strategy_class, delays):
    for delay in delays:
        print(f"Running backtest with {delay}-minute delay...")
        
        # Set the delay in the strategy class
        strategy_class.delay_minutes = delay

        # Create and configure the backtest
        bt = Backtest(data, strategy_class, cash=100000, commission=0.002)

        # Run the backtest and print the results
        stats = bt.run()
        print(stats)
        print("\n" + "="*50 + "\n")

# Define delay intervals in minutes
delays = [0, 2, 5, 10, 15, 30, 60]

# Run the alpha decay test
run_alpha_decay_test(data, DelayedLiquidationStrategy, delays)
