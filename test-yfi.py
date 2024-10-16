import yfinance as yf
import datetime

def test_download():
    symbol = 'BTC-USD'
    start = datetime.datetime(2020, 2, 1)
    end = datetime.datetime.now()
    
    print(f"Attempting to download data for {symbol} from {start} to {end}")
    df = yf.download(symbol, start=start, end=end, progress=True)
    
    if df.empty:
        print("Downloaded DataFrame is empty.")
    else:
        print("Downloaded DataFrame:")
        print(df.head())

if __name__ == "__main__":
    test_download()
