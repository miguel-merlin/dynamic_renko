import matplotlib.pyplot as plt
import mplfinance as mpf

# Plot the Candlestick data, the buy and sell signal markers
def plot_candlestick(df, symbol):
    # Plot the candlestick chart
    mpf.plot(df, type='candle', style='charles', datetime_format='%Y-%m-%d', xrotation=20,
             title=str(symbol + ' Candlestick Chart'), ylabel='Price', xlabel='Date', scale_width_adjustment=dict(candle=2))

# Plot the Renko Data.
def plot_renko(renko_df, symbol):
    # Plot the Renko Chart
    adp = [mpf.make_addplot(renko_df['buy_positions'], type='scatter', marker='^', label= "Buy", markersize=80, color='#2cf651'),
      mpf.make_addplot(renko_df['sell_positions'], type='scatter', marker='v', label= "Sell", markersize=80, color='#f50100')
     ]
    mpf.plot(renko_df, addplot=adp, type='candle', style='charles', datetime_format='%Y-%m-%d', xrotation=20,
             title=str(symbol + ' Renko Chart'), ylabel='Price', xlabel='Date', scale_width_adjustment=dict(candle=2))

# Plot the performance curve
def plot_performance_curve(strategy_df):
    # Plot the performance curve
    plt.plot(strategy_df['cumulative_balance'])
    plt.title('Performance Curve')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.xticks(rotation=70)
    plt.show()