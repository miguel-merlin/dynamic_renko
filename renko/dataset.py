import pandas as pd

def fetch_asset_data(symbol, start_date, interval, exchange):
    """
    Returns data as df
    Args:
        symbol: Asset pair (ETH, USDT)
        start_date: Start date of data
        interval: Interval it takes to generate a single candle
        exchange: Broker to fetch data from
    """
    # Convert start date to milliseconds stamp
    start_date_ms = exchange.parse8601(start_date)
    
    ohlcv = exchange.fetch_ohlcv(symbol, interval, since=start_date_ms)
    
    header = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df = pd.DataFrame(ohlcv, columns=header)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    return df