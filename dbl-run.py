#!/usr/bin/python3
from ichimoku import *
import sys



def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            raise Exception("Double comparison TA code, needs two tickers.")
        elif arguments == 2:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()
            print("Underlying: ",sys.argv[2])
            underlying = sys.argv[2].upper()

            tick = 'daily'
        elif arguments == 3: # OK parse out both, filename and option
            print("Currency: ",sys.argv[1])
            print("Underlying: ",sys.argv[2])
            print("Tick Value: ",sys.argv[3])
            currency = sys.argv[1].upper()
            underlying = sys.argv[2].upper()

            if sys.argv[3] == 'W' or sys.argv[3] == 'w':
                raise Exception("No weekly for yfinance plotting")
            # Show extended information like stops and sca charts.
            elif sys.argv[3].upper() == 'X':
                tick = 'daily'

            else:
                raise Exception("Invalid 3rd arg,  X for extended plots on daily.")
        else: # Anything else is false
            raise Exception("Invalid option x is valid for extended.")
        return currency,underlying,tick

'''                  --------    MAIN   ------                   '''

# Get teh args from teh cmmand line , the currency and the optional -w for weekly tick
currency_label,underlying_label,tick = parse_arguments()

# Kludge, import the one that is in line with the tick rate.
#if tick == 'weekly':
#        from ichimoku_wk import *
#else:
#        from ichimoku import *


# Open a file and write all of the lists to it row by row.
#filename = currency_label + '-ohcl.csv'


# Load Sample Data into a dataframe
#df = pd.read_csv('./sample-data/ohcl_sample.csv',index_col=0)
import pandas as pd
import yfinance as yf
import datetime # Need this here and not up top because of wildcard import of Ichimoku
import time
import requests
import io

start = datetime.datetime(2020,2,1)
#end = datetime.datetime(2022,4,29)

end = datetime.datetime.now()

# Treat the currency label as a list to patch it in.
Symbols = [currency_label] # ['XMR-USD']
Symbols_U = [underlying_label] # ['XMR-USD']

#print(Symbols,Symbols_U)
# create empty dataframe
stock_final = pd.DataFrame() 

# iterate over each symbol
for i in Symbols:  
    
    # print the symbol which is being downloaded
    print( str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)  
    
    try:
        # download the stock price 
        stock = []
        stock = yf.download(i,start=start, end=end, progress=False)
        
        # append the individual stock prices 
        if len(stock) == 0:
            None
        else:
            stock['Name']=i
            stock_final = stock_final.append(stock,sort=False)
    except Exception:
        None

#print(stock_final.head())

# Cut in the yfinace data read here...
# Use df rather than stock final.
df = stock_final.tail(800) # tail it so that they both line up.


# PASS 2 for UNDERLYING
# re-create empty dataframe
stock_final = pd.DataFrame() 

# iterate over each symbol
for i in Symbols_U:  
    
    # print the symbol which is being downloaded
    print( str(Symbols_U.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)  
    
    try:
        # download the stock price 
        stock = []
        stock = yf.download(i,start=start, end=end, progress=False)
        
        # append the individual stock prices 
        if len(stock) == 0:
            None
        else:
            stock['Name']=i
            stock_final = stock_final.append(stock,sort=False)
    except Exception:
        None

#print(stock_final.head())
print(df.tail()) # Sanity check

# Cut in the yfinace data read here...
# Use dfu rather than stock final. dfu is for the underlying
dfu = stock_final.tail(800) # tail it so they line up.

# Get the final values which are derived by dividing out the two df's.
# Divide out by columns to get currency/underlying results.
df['Open'] = df['Open']/dfu['Open']
df['Close'] = df['Close']/dfu['Close']
df['High'] = df['High']/dfu['High']
df['Low'] = df['Low']/dfu['Low']
df['Adj Close'] = df['Adj Close']/dfu['Adj Close']

# Ichimoku needs a column with Date so set index to Date column.
# A bit of a hack but works OK.
df.reset_index(inplace=True)
#df.shift(periods=17000,axis=0)

df = df.rename(columns = {'index':'Date'})
df.shift(periods=17000,axis=0)


#df.shift(periods=17000)
# Cut in the yfinace data read here...
print(dfu.tail()) # Sanity check
print(df.tail()) # Sanity check


# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()

# Plot ichimoku
i.plot_ichi(currency_label,underlying_label)


if tick == 'daily':
        i.plot_bb(currency_label,underlying_label)
        # Extended plots...
        if len(sys.argv) == 4:
                if sys.argv[3].upper() == 'X':  
                        i.plot_stops(currency_label,underlying_label)
                        i.plot_long_bb(currency_label,underlying_label)



