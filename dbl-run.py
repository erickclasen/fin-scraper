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
            elif sys.argv[3].upper() == 'X' or sys.argv[3].upper() == 'I':
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


lookback_in_days = 365*2 # Two years of data to scrape.
# End the data on today.
end = datetime.datetime.now()

# Subtract lookback (two years) from today's date
start = end - datetime.timedelta(days=lookback_in_days)


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
# Divide out by columns to get currency/underlying results. Do it inplace, results to df.
df['Open'] = df['Open']/dfu['Open']
df['Close'] = df['Close']/dfu['Close']
df['High'] = df['High']/dfu['High']
df['Low'] = df['Low']/dfu['Low']
df['Adj Close'] = df['Adj Close']/dfu['Adj Close']


# Ichimoku needs a column with Date that is a series of numbers so reset index. Date becomes its
# own column.
# A bit of a hack but works OK.
df.reset_index(inplace=True)


# Offset the index to bring it up to the current date, it is a hack but needed as 
# the ichimonk code usees the index number as the date while the yfinance data has a normal
# formatted date for a date, like 2023-02-06.

# Calculate the number of days between the two dates
start_date = datetime.datetime(1970, 1, 1) # Linux start date.
end_date = datetime.datetime.now() # Today

# Need to fudge up the index todays date, minus the Linux Start, minus the lookback period, 2 years.
offset = (end_date - start_date).days - lookback_in_days + 1

# Finally offset the index
df.index = df.index + offset

# Cut in the yfinace data read here...
print(dfu.tail()) # Sanity check
print(df.tail()) # Sanity check


# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()

# Plot ichimoku
i.plot_ichi(currency_label,underlying_label)

# Ichimoku Summary plot mode, only print Ichimoku.
if len(sys.argv) == 4 and sys.argv[3].upper() == 'I':  
	quit()


if tick == 'daily':
        i.plot_bb(currency_label,underlying_label)
        # Extended plots...
        if len(sys.argv) == 4:
                if sys.argv[3].upper() == 'X':  
                        i.plot_stops(currency_label,underlying_label)
                        i.plot_long_bb(currency_label,underlying_label)



