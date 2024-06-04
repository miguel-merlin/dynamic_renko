import ccxt

# Define class as Singleton
class RenkoAlgo(object):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RenkoAlgo, cls).__new__(cls)        
        return cls._instance
    
    def __init__(self, symbol, start_data, interval) -> None:
        self.symbol = symbol
        self.start_data = start_data
        self.interval = interval
        self.exchange = ccxt.kraken()