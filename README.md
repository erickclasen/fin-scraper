# fin-scraper
Uses yfinance module as a frontend for Ichimoku, 20 day + 200 day Bollinger Bands and stop-loss charts
## Requirements
Requires
* yfinance
*  pandas
*  numpy
*  matplotlib

# What it is
This is a merge between a frontend that scrapes financial data using yfinance and a plotting backend that plots prices. It is quick and dirty code. Allows plotting of any tickers that are on Yahoo Finance. Ones that can be found there or on any app that gets this data like on iPhone, iPad the built in stock app. Also covers many cryptos as well. It can plot the ticker or compare two of them and get things like...
* Gold/Silver ratio ./dbl-run.py gc=f si=f
* ETH/BTC  ./dbl-run.py eth-usd btc-usd
* Stock Pairs
* Assets against a market, like Apple vs SP500    ./dbl-run.py aapl spy
* Just plain stocks obviously, like     ./run.py msft

Charts have
* Price Close, High and Low
* 10 day low and 60 day high
* Monthly high and low bands
* For Ichimoku, Tenken, Kijun, Chikou Span, Cloud ( doubled settings)
* 20 and 60 day moving averages
* Bollinger bands with 20 day average and 1,1.5,2 standard deviations
* Long Bollinger bands with 200 day average and 1,1.5,2 standard deviations
* 50 day moving average for long BOllinger Bands
* Stop loss suggestion plot with 10 day low and 1 and 2 standard deviations off of 5 day moving average

## Usage Example
./run.py btc-usd
Works with lower or upper case input as it uses toupper.
This will plot an Ichimoku chart and 20 Day Bollinger Bands chart.
Note: The Ichimoku chart is clipped to todays date, it does not go into the "future". This is an issue with the dating.
Date Issue: The dates are derived from the Index and have an issue as day 1 is 1/1/1970. Not sure how to easily fix this. Spent way more time trying than it took to build this little hack-merge.

Prices are show with a solid green band for close price and grey green bands for high and low. Originally used mplfinance but this stopped working at some point so went with a price and bands scheme. See the legend for what the lines are.

./run.py btc-usd x
This is an extended mode which will also plot suggested stop loss prices based on the lowest 10 day prices and one standard deviation from a 5 day SMA of price.
It also plots what I have called Long Bollinger Bands, which are 200 day versions of the Bollinger Bands. This can be a tool to see when it is best to DCA (Dollar Cost Average) in and out of an asset over a long time frame. It also has a yellow 5 day SMA plot on it as an optional filter that states that price must below this as well for confirmation. THe inverse applies to DCA'ing out on peaks. It has 1,1.5 and 2 standard deviations marked off.

./dbl-run.py pep ko
Double run is just like the single run expect it takes two assets like Coca-Cola and Pepsi and compares them. This could be used to see when it is a good time to sell one into the other or for hedging for example. Not advice, just ideas.

## Sources
Not sure who to credit on the initial Ichimoku code that I modded. TBD: Look for clues in my codebase history.
TBD: Source for yfinance code frontend.
