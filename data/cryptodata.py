from tqdm import tqdm
import pandas as pd
import datetime
import os
import ccxt
from math import ceil


symbol = 'BTC/USDT'
timeframe = '1m' 
weeks = 100


# Function to convert timeframe to seconds
def timeframe_to_sec(timeframe):
    if 'm' in timeframe:
        return int(''.join([char for char in timeframe if char.isnumeric()])) * 60
    elif 'h' in timeframe:
        return int(''.join([char for char in timeframe if char.isnumeric()])) * 60 * 60
    elif 'd' in timeframe:
        return int(''.join([char for char in timeframe if char.isnumeric()])) * 24 * 60 * 60


def get_historical_data(symbol, timeframe, weeks):
    filename = f'{symbol.replace("/", "")}-{timeframe}-{weeks}wks-data.csv'

    # Check if the file already exists
    if os.path.exists(filename):
        print(f"Data already exists at {filename}. Loading from file.")
        return pd.read_csv(filename, parse_dates=['datetime'], index_col='datetime')

    # Configure the CCXT exchange
    coinbase = ccxt.coinbase({
        'apiKey': os.getenv('COINBASE_API_KEY'),
        'secret': os.getenv('COINBASE_API_SECRET'),
        'enableRateLimit': True,
    })

    granularity = timeframe_to_sec(timeframe)  # Convert timeframe to seconds
    total_time = weeks * 7 * 24 * 60 * 60
    run_times = ceil(total_time / (granularity * 200))  # Calculate number of API calls needed

    dataframe = pd.DataFrame()

    # Fetch historical data
    for i in tqdm(range(run_times), desc="Fetching data"):
        since = datetime.datetime.utcnow() - datetime.timedelta(seconds=granularity * 200 * (i + 1))
        since_timestamp = int(since.timestamp()) * 1000  # Convert to milliseconds

        try:
            data = coinbase.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=200)
            if not data:
                continue
            df = pd.DataFrame(data, columns=['datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
            df['datetime'] = df['datetime'].dt.floor('s')
            dataframe = pd.concat([df, dataframe])
        except Exception as e:
            print(f"Error fetching data: {e}")
            continue

    # Process and save the data
    if dataframe.empty:
        raise ValueError("No data fetched from the API. Check your parameters or API limits.")

    dataframe = dataframe.set_index('datetime')
    dataframe = dataframe[["Open", "High", "Low", "Close", "Volume"]]
    dataframe.to_csv(filename)
    print(f"Data saved to {filename}")

    return dataframe


# Main execution
if __name__ == "__main__":
    try:
        df = get_historical_data(symbol, timeframe, weeks)
        print(df.head())
    except Exception as e:
        print(f"An error occurred: {e}")
