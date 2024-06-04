import pandas_ta as ta
from stocktrends import Renko
import numpy as np
import scipy.optimize as opt
import pandas as pd

def renko_data(data):
    """
    Calculate the Renko chart data given the asset data
    """
    # For stable backtesting, the last row is dropped (Completed candles)
    data.drop(data.index[-1], inplace=True)
    
    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], 14)
    data.dropna(inplace=True)
    
    def evaluate_brick_size_atr(brick_size, atr_values):
        # Calculate number of bricks based on ATR size
        num_bricks = atr_values // brick_size
        return np.sum(num_bricks)

    # Get optimized brick size
    brick = opt.fminbound(lambda x: -evaluate_brick_size_atr(x, data['ATR']), np.min(data['ATR']), np.max(data['ATR']), disp=0)
    
    def custom_round(number):
        # List of available rounding values
        rounding_values = [0.001, 0.005, 0.01, 0.05,
                           0.1, 0.5, 1] + list(range(5, 100, 5))
        rounding_values += list(range(100, 1000, 50)) + \
            list(range(1000, 10000, 100))
        
        # Find the closest value to the number
        return min(rounding_values, key=lambda x: abs(x - number))

    brick_size = custom_round(brick)
    print(f"Optimized brick size: {brick_size}")
    data.reset_index(inplace=True)
    data.columns = [i.lower() for i in data.columns]
    df = Renko(data)
    df.brick_size = brick_size
    renko_df = df.get_ohlc_data()
    
    renko_df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, inplace=True)
    
    # Return the ohlc columns to floats
    renko_df['Open'] = renko_df['Open'].astype(float)
    renko_df['High'] = renko_df['High'].astype(float)
    renko_df['Low'] = renko_df['Low'].astype(float)
    renko_df['Close'] = renko_df['Close'].astype(float)
    
    return renko_df

def generate_positions(renko_df):
    # Rename the index of the renko data to brick
    renko_df.index.name = "brick"

    # Initialize signals list with 0 (no signal) for the first brick
    signals = []

    for i in range(0, len(renko_df)):
        # Get the current and previous brick colors
        is_current_green = renko_df['Close'].iloc[i] > renko_df['Open'].iloc[i]
        is_prev_green = renko_df['Close'].iloc[i -
                                               1] > renko_df['Open'].iloc[i - 1]

        if is_current_green and not is_prev_green:
            signals.append(1)  # Buy signal when the brick changes to green
        elif is_current_green and is_prev_green:
            signals.append(1)  # Hold signal when the brick remains green
        elif not is_current_green and is_prev_green:
            signals.append(-1)  # Sell signal when the brick changes to red
        elif not is_current_green and not is_prev_green:
            signals.append(-1)  # Hold signal when the brick remains red

     # Add the 'signals' column to the DataFrame
    renko_df['signals'] = signals
    renko_df['signals'] = renko_df["signals"].shift(1) #Remove look ahead bias
    renko_df.fillna(0.0, inplace=True)
    renko_df.set_index("Date", inplace=True)
    
    # Create the Positions
    # Initialize positions with nan
    renko_df['buy_positions'] = np.nan
    renko_df['sell_positions'] = np.nan
    
    renko_df.index.freq = pd.infer_freq(renko_df.index)
    
   # Update the buy_positions with the close price where the signal is 1 and the previous signal is not equal to the current signal
    buy_signal_indices = renko_df[(renko_df['signals'] == 1) & (renko_df['signals'] != renko_df['signals'].shift(1))].index
    renko_df.loc[buy_signal_indices, 'buy_positions'] = renko_df.loc[buy_signal_indices, 'Close']

    # Update the sell_positions with close price where the signal is -1 and the previous signal is not equal to the current signal
    sell_signal_indices = renko_df[(renko_df['signals'] == -1) & (renko_df['signals'] != renko_df['signals'].shift(1))].index
    renko_df.loc[sell_signal_indices, 'sell_positions'] = renko_df.loc[sell_signal_indices, 'Close']

    # Reset duplicate dates in the positions to nan, i.e where the previous date is equal to the current date
    renko_df.loc[renko_df.index == pd.Series(renko_df.index).shift(1), ['buy_positions', 'sell_positions']] = np.nan

    return renko_df
