import ccxt
from dataset import fetch_asset_data
from renko import renko_data, generate_positions
from performance import calculate_strategy_performance
from plots import plot_candlestick, plot_renko, plot_performance_curve

def main():
    symbol = "ETH/USDT"
    start_date = "2010-12-1"
    interval = '4h'
    exchange = ccxt.kraken()
    
    # Fetch the asset data
    data = fetch_asset_data(symbol=symbol, start_date=start_date, interval=interval, exchange=exchange)
    
    # Print the asset dataframe
    print(data)
    
    # Plot the Symbol data candlestick chart
    plot_candlestick(df=data)

    # Get the Renko Bricks
    renko_df = renko_data(data)
    print(renko_df)

    # Generate Strategy Signals
    positions_df = generate_positions(renko_df)
    print(positions_df)

    # Plot the Renko Bricks and Positions
    plot_renko(renko_df)

    # Calculate Strategy Performance
    strategy_df = calculate_strategy_performance(positions_df)
    print(strategy_df)

    # Plot the performance curve
    plot_performance_curve(strategy_df)