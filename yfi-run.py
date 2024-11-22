#!/usr/bin/python3
from yfiichimoku import Ichimoku
import sys
import pandas as pd
import yfinance as yf
import datetime

def parse_arguments():
    arguments = len(sys.argv) - 1 # Don't count the filename as an arg.

    # Currency is always the first argument.
    currency = sys.argv[1].upper()

    # This is the logic to handle all the types of args.
    # Ex 1 = run.py btc-usd
    # Ex 2 = run.py btc-usd x or run.py gc=f si=f
    # Ex 3 = run.py ko pep i
    if arguments == 1: # Currency only
        underlying = None
        extended_arguments = None
    elif arguments == 2: # ...underlying or extended args, like X or I.
        test_value = sys.argv[2].upper()
        if test_value in ('X', 'I'): # Extended Args.
                extended_arguments = test_value
                underlying = None
        else: # Underlying Currency
                underlying = test_value
                extended_arguments = None
    elif arguments == 3: # ... underlying AND extended arguments.
        underlying = sys.argv[2].upper()
        test_value = sys.argv[3].upper()
        if test_value in ('X', 'I'):
                extended_arguments = test_value
        else: 
                raise Exception("Double comparison TA code, incorrect 3rd argument, X or I acceptable.")
    
    return currency, underlying, extended_arguments

def download_data(symbols, start, end):
    stock_list = []
    
    for i in symbols:  
        print(f"Downloading {i}...", end=' ', flush=True)
        try:
            stock = yf.download(i, start=start, end=end, progress=False)
            if not stock.empty:
                stock['Name'] = i  # Add a 'Name' column to identify the symbol
                stock_list.append(stock)
            else:
                print(f"No data returned for {i}")
        except Exception as e:
            print(f"Error downloading {i}: {e}")
    
    if stock_list:
        stock_final = pd.concat(stock_list, sort=False)
        print("\nConcatenated DataFrame Head/Tail:")
        print(stock_final.head(5))  # Debugging: Print the first few rows
        print(stock_final.tail(5))  # Debugging: Print the last few rows

        return stock_final
    else:
        print("No valid data downloaded.")
        sys.exit(1)

def main():
    # Parse command-line arguments
    currency_label, underlying_label, extended_arguments = parse_arguments()
    
    # Define the date range
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=730)  # Go back 2 years (365 * 2 days)

    # Download currency and underlying asset data
    currency_data = download_data([currency_label], start, end)

    # Test to see if there is an underlying currency, if yes, download and divide into currency.
    if underlying_label != None:
            underlying_data = download_data([underlying_label], start, end)

            # Calculate final values by dividing the two DataFrames
            for col in ['Open', 'Close', 'High', 'Low', 'Adj Close']:
                currency_data[col] = currency_data[col] / underlying_data[col]

            # Sanity check on the results
            print("\nFinal Calculated DataFrame Head:")
            print(currency_data.head())  # Debugging: Print the first few rows

    else:
            # Set underlying_label as blank (not used)
            underlying_label = ""

    # Initialize Ichimoku with the OHLC DataFrame
    ichimoku = Ichimoku(currency_data)
    ichimoku_df = ichimoku.run()

    # Plot Ichimoku, always
    ichimoku.plot_ichi(currency_label, underlying_label)

    # Extended plot options
    if extended_arguments != 'I': # Plot bbands when not using extended arg I
            ichimoku.plot_bb(currency_label, underlying_label)
    if extended_arguments == 'X': # Plot everything available. 
            ichimoku.plot_stops(currency_label, underlying_label)
            ichimoku.plot_long_bb(currency_label, underlying_label)

if __name__ == "__main__":
    main()
