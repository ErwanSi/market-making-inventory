import ccxt
import pandas as pd
import time
from datetime import datetime
import os

class BinanceDataFetcher:
    """
    Fetches historical market data from Binance using CCXT.
    """
    
    def __init__(self, symbol='BTC/USDT', timeframe='1m'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
        })
        
    def fetch_historical_data(self, limit=1000):
        """
        Fetch OHLCV data.
        Returns a DataFrame with ['time', 'open', 'high', 'low', 'close', 'volume'].
        """
        print(f"Fetching {limit} candles for {self.symbol} ({self.timeframe})...")
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['time'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Save for caching
            os.makedirs("data", exist_ok=True)
            filename = f"data/{self.symbol.replace('/', '_')}_{self.timeframe}.csv"
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
            
            return df
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            # Try to load cached
            filename = f"data/{self.symbol.replace('/', '_')}_{self.timeframe}.csv"
            if os.path.exists(filename):
                print("Loading cached data instead.")
                return pd.read_csv(filename)
            else:
                raise e

    def get_price_path(self, limit=1000):
        """
        Returns numpy array of close prices for simulation.
        """
        df = self.fetch_historical_data(limit)
        return df['close'].values
