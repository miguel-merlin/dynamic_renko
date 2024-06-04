import ccxt
from algorithm.dataset import fetch_asset_data
from algorithm.renko import renko_data, generate_positions
from algorithm.performance import calculate_strategy_performance

# Define class as Singleton
class RenkoAlgo(object):
    _instance = None
    
    def __new__(cls, symbol, start_date, interval):
        if cls._instance is None:
            cls._instance = super(RenkoAlgo, cls).__new__(cls)        
            cls._instance.symbol = symbol
            cls._instance.start_date = start_date
            cls._instance.interval = interval
            cls._instance.exchange = ccxt.kraken()
            cls._instance._refetch_data_and_compute_renko()
        return cls._instance
    
    def _refetch_data_and_compute_renko(self):
        self.data = fetch_asset_data(symbol=self.symbol, start_date=self.start_date, interval=self.interval, exchange=self.exchange)
        self.renko_df = renko_data(self.data)
        self.positions_df = generate_positions(self.renko_df)
        self.strategy_df = calculate_strategy_performance(self.positions_df)
    
    def set_symbol(self, symbol):
        self.symbol = symbol
        self._refetch_data_and_compute_renko()
    
    def set_start_date(self, start_date):
        self.start_date = start_date
        self._refetch_data_and_compute_renko()
    
    def set_interval(self, interval):
        self.interval = interval
        self._refetch_data_and_compute_renko()
        
    def get_candlestick_plot(self):
        return self.data
    
    def get_renko_plot(self):
        return self.renko_df

    def get_performance_curve(self):
        return self.strategy_df