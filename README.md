# fin-scraper
Uses yfinance module as a frontend for Ichimoku, 20 day + 200 day Bollinger Bands and stop-loss charts
## Requirements
Requires
* yfinance
*  pandas
*  numpy
*  matplotlib

``` pip3 install -U yfinance ```

``` pip3 install -U pandas ```

``` pip3 install -U numpy ```

``` pip3 install -U matplotlib ```

## What it is
This is a merge between a frontend that scrapes financial data using yfinance and a plotting backend that plots prices. It is quick and dirty code. Allows plotting of any tickers that are on Yahoo Finance. Ones that can be found there or on any app that gets this data like on iPhone, iPad the built in stock app. Also covers many cryptos as well. It can plot the ticker or compare two of them and get things like...
* Gold/Silver ratio ``` ./dbl-run.py gc=f si=f ```
* ETH/BTC  ``` ./dbl-run.py eth-usd btc-usd ```
* Stock Pairs like Coca-Cola -v- Pepsi  ``` ./dbl-run.py ko pep ```
* Assets against a market, like Apple vs SP500   ``` ./dbl-run.py aapl spy ```
* Just plain stocks obviously, like   ``` ./run.py msft ```

### Charts have
* Price Close, High and Low
* 10 day low and 60 day high, breakout and stop loss
* For Ichimoku, Tenken, Kijun, Chikou Span, Cloud ( doubled settings)
* 20 and 60 day moving averages
* Bollinger bands with 20 day average and 1,2 standard deviations
* Long Bollinger bands with 200 day average and 1,1.5,2 standard deviations
* 50 day moving average for long Bollinger Bands
* Stop loss suggestion plot with 10 day low and 1 and 2 standard deviations off of 5 day moving average
* 30 day price channels

## Usage Examples

### Single Run
``` ./run.py btc-usd ```

Works with lower or upper case input as it uses toupper.
This will plot an Ichimoku chart and 20 Day Bollinger Bands chart.
Note: The Ichimoku chart is clipped to todays date, it does not go into the "future". This is an issue with the dating, still figuring it out, any input would be helpful.
Date Issue: Dates line up fine for crypto and anything that tades 24/7, the dates on the chart are offset for other things like stocks that trade 5 days a week. This offset is due to skewing of the index count. Hard to fix this, just FYI and beware of this. The right end of the chart is always "today". Would love to solve this 100%, any ideas are welcome. (*Spent way more time trying than it took to build this little hack-merge.*) The charts shown as examples on this page are from before the fix, so dates are offset far.
![BTC-USD -ichimoku](https://user-images.githubusercontent.com/51176457/167054060-2dbf3fd5-4eab-43be-89b2-297b33915db3.png)
![BTC-USD -bbands](https://user-images.githubusercontent.com/51176457/167054055-9c11d156-4b74-47cb-ab9e-4aaec828f808.png)

Prices are show with a solid green band for close price and grey green bands for high and low. Originally used mplfinance but this stopped working at some point so went with a price and bands scheme. See the legend for what the lines are.

### Single Run - Extended Charts
``` ./run.py btc-usd x ```

This is an extended mode which will also plot suggested stop loss prices based on the lowest 10 day prices and one standard deviation from a 5 day SMA of price.
It also plots what I have called Long Bollinger Bands, which are 200 day versions of the Bollinger Bands. This can be a tool to see when it is best to DCA (Dollar Cost Average) in and out of an asset over a long time frame. It also has a yellow 5 day SMA plot on it as an optional filter that states that price must below this as well for confirmation. THe inverse applies to DCA'ing out on peaks. It has 1,1.5 and 2 standard deviations marked off.
![BTC-USD -stops](https://user-images.githubusercontent.com/51176457/167054061-d3ebb586-f205-4097-bb47-1795e2bef552.png)
![BTC-USD-long-bbands](https://user-images.githubusercontent.com/51176457/167054063-841918f2-4f0a-4563-841a-547c9e19fdfa.png)

### Double Run

``` ./dbl-run.py ko pep ```

Double run is just like the single run expect it takes two assets like Coca-Cola and Pepsi and compares them. This could be used to see when it is a good time to sell one into the other or for hedging for example. Not advice, just ideas.

![KO PEP-ichimoku](https://user-images.githubusercontent.com/51176457/167054066-b4336e87-5e58-4f3b-8d9a-d68f5b7ad650.png)
![KO PEP-bbands](https://user-images.githubusercontent.com/51176457/167054065-f28b6d5d-8b87-49f7-a2aa-00ef2fd2308f.png)

### Double Run - Extended Charts

``` ./dbl-run.py ko pep x ```

![KO PEP-stops](https://user-images.githubusercontent.com/51176457/167054069-ff34cc64-c423-42f3-a1f1-c74f7257d90c.png)
![KO-long-bbands](https://user-images.githubusercontent.com/51176457/167054070-3b8cd741-3dde-456a-8864-7410e3dfbcb8.png)

## Sources
Not sure who to credit on the initial Ichimoku code that I modded. TBD: Look for clues in my codebase history.
TBD: Source for yfinance code frontend.
