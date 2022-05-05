# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
#from mplfinance import candlestick_ohlc
#import mplfinance

import matplotlib.pyplot as plt
import numpy as np
import decimal
import os

class Ichimoku():
    """
    @param: ohcl_df <DataFrame> 

    Required columns of ohcl_df are: 
        Date<Float>,Open<Float>,High<Float>,Close<Float>,Low<Float>
    """
    def __init__(self, ohcl_df):
        self.ohcl_df = ohcl_df

    def run(self):
        tenkan_window = 20
        kijun_window = 60
        senkou_span_b_window = 120
        cloud_displacement = 30
        chikou_shift = -30
        ohcl_df = self.ohcl_df

        # Dates are floats in mdates like 736740.0
        # the period is the difference of last two dates
        #last_date = ohcl_df["Date"].iloc[-1]
        #period = last_date - ohcl_df["Date"].iloc[-2]

        # Add rows for N periods shift (cloud_displacement)
        #ext_beginning = decimal.Decimal((last_date+period).item())
        #ext_end = decimal.Decimal((last_date + ((period*cloud_displacement)+period)).item())
        #dates_ext = list(self.drange(ext_beginning, ext_end, str(period)))
        #dates_ext_df = pd.DataFrame({"Date": dates_ext})
        #dates_ext_df.index = dates_ext # also update the df index
        #ohcl_df = ohcl_df.append(dates_ext_df)

        # Tenkan 
        tenkan_sen_high = ohcl_df['High'].rolling( window=tenkan_window ).max()
        tenkan_sen_low = ohcl_df['Low'].rolling( window=tenkan_window ).min()
        ohcl_df['tenkan_sen'] = (tenkan_sen_high + tenkan_sen_low) /2
        # Kijun 
        kijun_sen_high = ohcl_df['High'].rolling( window=kijun_window ).max()
        kijun_sen_low = ohcl_df['Low'].rolling( window=kijun_window ).min()
        ohcl_df['kijun_sen'] = (kijun_sen_high + kijun_sen_low) / 2
        # Senkou Span A 
        ohcl_df['senkou_span_a'] = ((ohcl_df['tenkan_sen'] + ohcl_df['kijun_sen']) / 2).shift(cloud_displacement)
        # Senkou Span B 
        senkou_span_b_high = ohcl_df['High'].rolling( window=senkou_span_b_window ).max()
        senkou_span_b_low = ohcl_df['Low'].rolling( window=senkou_span_b_window ).min()
        ohcl_df['senkou_span_b'] = ((senkou_span_b_high + senkou_span_b_low) / 2).shift(cloud_displacement)
        # Chikou
        ohcl_df['chikou_span'] = ohcl_df['Close'].shift(chikou_shift)

        self.ohcl_df = ohcl_df
        return ohcl_df

    def plot_ichi(self,currency_label,underlying_label):
        fig, ax = plt.subplots()    
        self.plot_candlesticks(fig, ax)
        self.plot_channels(fig, ax)
        self.plot_ichimoku(fig, ax)
        #self.plot_bbands(fig, ax)

        self.pretty_plot(fig, ax,currency_label,underlying_label)
        save_fig(currency_label+"."+underlying_label+"-ichimoku")
        plt.show()

    def plot_bb(self, currency_label,underlying_label):
        fig, ax = plt.subplots()    
        self.plot_candlesticks(fig, ax)
        self.plot_channels(fig, ax)
        #self.plot_ichimoku(fig, ax)
        self.plot_bbands(fig, ax)

        self.pretty_plot(fig, ax,currency_label,underlying_label,title=' Bollinger Bands Chart: Daily')
        save_fig(currency_label+"."+underlying_label+"-bbands")
        plt.show()

    def plot_long_bb(self, currency_label,underlying_label):
        fig, ax = plt.subplots()    
        self.plot_candlesticks(fig, ax)
        self.plot_channels(fig, ax)
        #self.plot_ichimoku(fig, ax)
        self.plot_long_bbands(fig, ax)

        self.pretty_plot(fig, ax,currency_label,underlying_label,title=' LONG Bollinger Bands Chart: Daily')
        save_fig(currency_label+"-long-bbands")
        plt.show()


    """ This is the new plot stops part for plotting the trailing stop losses, this uses a 10d low price channel and a version of a lower bband that is modded.
        The idea is to print out buy and sell stops as the 60 and 10 day price channels off of the highs and lows and volatility stops based on lower bbands,
        except using the current price which is really a 5 day average for a lower volt stops, 1SD and 2SD. THen subjective discrection is used to pick the 
        right stops. Usually the lower of the 2 is acceptable, except in fast moving markets, when tight stops are smarter, or just set targets.
         THe Price channels should be such as to line up fairly well with the William's fractals in theory."""
    def plot_stops(self, currency_label,underlying_label):
        fig, ax = plt.subplots()    
        self.plot_candlesticks(fig, ax)

        # For the stops uses the breakout channels
        self.plot_break_out_channels(fig, ax)

        self.plot_stopbands(fig, ax)

        self.pretty_plot(fig, ax,currency_label,underlying_label,title=' Trailing Stoploss and Breakout Channel Chart: Daily')
        save_fig(currency_label+"."+underlying_label+"-stops")
        plt.show()        



    def pretty_plot(self, fig, ax,currency_label,underlying_label,title = ' Clipped Ichimoku Cloud Chart: Daily'):
        ax.legend()
        fig.autofmt_xdate()
        ax.xaxis_date()

        # Chart info
        #title = 'Ichimoku Cloud Chart (Currency)'
        bgcolor = '#131722'
        grid_color = '#363c4e'
        spines_color = '#d9d9d9'
        # Axes
        plt.title(currency_label+"."+underlying_label+" "+title, color='white')
        plt.xlabel('Date', color=spines_color, fontsize=20)
        plt.ylabel('Price', color=spines_color, fontsize=20)
        #ax.set_axis_bgcolor(bgcolor)
        #ax.set_facecolor('#131722') Does not work with my matplotlib setup.
        ax.grid(linestyle='-', linewidth='1.0', color=grid_color)
        ax.yaxis.tick_right()
        ax.set_yscale("linear") # , nonposy='clip'
        fig.patch.set_facecolor(bgcolor)
        fig.patch.set_edgecolor(bgcolor)
        plt.rcParams['figure.facecolor'] = bgcolor
        plt.rcParams['savefig.facecolor'] = bgcolor
        ax.spines['bottom'].set_color(spines_color)
        ax.spines['top'].set_color(spines_color) 
        ax.spines['right'].set_color(spines_color)
        ax.spines['left'].set_color(spines_color)
        ax.tick_params(axis='x', colors=spines_color, size=20)
        ax.tick_params(axis='y', colors=spines_color, size=20)
        fig.tight_layout()
        ax.autoscale_view()

    def plot_ichimoku(self, fig, ax, view_limit=100):
        d2 = self.ohcl_df.loc[:, ['tenkan_sen','kijun_sen','senkou_span_a','senkou_span_b', 'chikou_span']]
        d2 = d2.tail(view_limit)
        #date_axis = self.ohcl_df['Date'].tail(view_limit) #d2.index.values
        date_axis = d2.index.values #+17000 does not work right this way!!
        #print(date_axis)
        #quit()

        # ichimoku
        plt.plot(date_axis, d2['tenkan_sen'], label="tenkan", color='#0496ff', alpha=0.65,linewidth=1.5)
        plt.plot(date_axis, d2['kijun_sen'], label="kijun", color="#991515", alpha=0.65,linewidth=1.5)
        plt.plot(date_axis, d2['senkou_span_a'], label="span a", color="#008000", alpha=0.65,linewidth=0.95)
        plt.plot(date_axis, d2['senkou_span_b'], label="span b", color="#ff0000", alpha=0.65, linewidth=0.95)
        plt.plot(date_axis, d2['chikou_span'], label="chikou", color="#808080", alpha=0.65, linewidth=0.75)
        #plt.plot(date_axis, d2['chikou_span'], label="chikou", color="#000000", alpha=0.65, linewidth=0.95)

        # green cloud
        ax.fill_between(date_axis, d2['senkou_span_a'], d2['senkou_span_b'], where=d2['senkou_span_a']> d2['senkou_span_b'], facecolor='#008000', interpolate=True, alpha=0.25)
        # red cloud
        ax.fill_between(date_axis, d2['senkou_span_a'], d2['senkou_span_b'], where=d2['senkou_span_b']> d2['senkou_span_a'], facecolor='#ff0000', interpolate=True, alpha=0.25)

    def plot_candlesticks(self, fig, ax, view_limit=100):
        # plot candlesticks
        candlesticks_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        candlesticks_df = candlesticks_df.tail(view_limit)
        #print(ax,candlesticks_df)
        #quit()
        # plot candlesticks
        #mplfinance.plot(ax, candlesticks_df.values, width=0.9, colorup='#83b987', colordown='#eb4d5c', alpha=0.5 )
        #mplfinance.plot(candlesticks_df)
        plt.plot(candlesticks_df['Close'], label="price", color='#00FF00', alpha=0.95,linewidth = 2.5)
        plt.plot(candlesticks_df['High'], color='#008000', alpha=0.5,linewidth = 1.5)
        plt.plot(candlesticks_df['Low'], color='#008000', alpha=0.5,linewidth = 1.5)

    def plot_channels(self, fig, ax, view_limit=100):
        # plot candlesticks
        chan_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        chan_df = chan_df.tail(view_limit)

        kijun_window = 30
        kijun_sen_high = chan_df['High'].rolling( window=kijun_window ).max()
        kijun_sen_low = chan_df['Low'].rolling( window=kijun_window ).min()
        mean20 = chan_df['Close'].rolling(20).mean()
        mean60 = chan_df['Close'].rolling(60).mean()

        plt.plot(kijun_sen_high, label="PC Hi 30", color='#004000', alpha=0.35,linewidth = 1.5, linestyle = '--')
        plt.plot(kijun_sen_low, label="PC Low 30", color='#004000', alpha=0.35,linewidth = 1.5, linestyle = '--')
        plt.plot(mean20, label="SMA20", color='#0496ff', alpha=0.35,linewidth = 1.5, linestyle = '--')
        plt.plot(mean60, label="SMA60", color="#991515", alpha=0.35,linewidth=1.5,linestyle = '--')


    def plot_bbands(self, fig, ax, view_limit=100):
        # plot bbands
        bb_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        bb_df = bb_df.tail(view_limit)

        mean = bb_df['Close'].rolling(20).mean()
        bb_high = mean + 1.96*bb_df['High'].rolling(20).std()
        bb_low = mean - 1.96*bb_df['Low'].rolling(20).std()
        # Inner 1 std dev lines, halfway to bbands
        bb_high_1 = mean + 1.0*bb_df['High'].rolling(20).std()
        bb_low_1 = mean - 1.0*bb_df['Low'].rolling(20).std()

        plt.plot(bb_high, label="BB Hi ", color='#FF0000', alpha=0.95,linewidth = 3.5, linestyle = '--')
        plt.plot(bb_low, label="BB Low", color='#FF0000', alpha=0.95,linewidth = 3.5, linestyle = '--')

        # Inner 1 std dev lines, halfway to bbands
        plt.plot(bb_high_1, label="BB Hi 1", color='#FF1010', alpha=0.65,linewidth = 1.5, linestyle = '--')
        plt.plot(bb_low_1, label="BB Low 1", color='#FF1010', alpha=0.65,linewidth = 1.5, linestyle = '--')

        plt.plot(mean, label="SMA20", color='#FF1010', alpha=0.95,linewidth = 3.5, linestyle = '-')




    def plot_break_out_channels(self, fig, ax, view_limit=100):
        # plot candlesticks
        chan_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        chan_df = chan_df.tail(view_limit)

        # The windows for the channels.
        hi_window = 60
        lo_window = 10
        
        # Channels for NDBO buy and Sell
        high_chan = chan_df['High'].rolling( window=hi_window ).max()
        low_chan = chan_df['Low'].rolling( window=lo_window ).min()


        plt.plot(high_chan, label="Buy BK PC Hi "+str(hi_window), color='#004000', alpha=0.35,linewidth = 2.5, linestyle = '--')
        plt.plot(low_chan, label="Sell BK PC Low "+str(lo_window), color='#004000', alpha=0.35,linewidth = 2.5, linestyle = '--')


    def plot_stopbands(self, fig, ax, view_limit=100):
        # plot bbands

        bb_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        bb_df = bb_df.tail(view_limit)

        # Take a 5 day mean as a price proxy. The average is a lot less jagged than the actual price.
        price_now = bb_df['Close'].rolling(5).mean()

        # 2 trailing volat stops, acts like the lower BBands at 2SD with a mid point marker at 1SD.
        # EXCEPT, this uses the price_now AND not the 20 day SMA of price, uses 5 day SMA as proxy for price as it is smoother.
        #Stop loss os the same distance from price as a bb, except off of the low. bb_high = mean + 1.96*bb_df['High'].rolling(20).std()
        stop_loss = price_now - 1.96*bb_df['Low'].rolling(20).std()
        
        # Inner 1 std dev lines, halfway to bband low for stop loss.
        stop_loss_1 = price_now - 1.0*bb_df['Low'].rolling(20).std()

        
        plt.plot(stop_loss, label="2SD Stop Loss", color='#FF0000', alpha=0.95,linewidth = 3.5, linestyle = '--')

        # Inner 1 std dev lines, halfway to bbands
        plt.plot(stop_loss_1, label="1SD Stop Loss", color='#FF1010', alpha=0.65,linewidth = 1.5, linestyle = '--')


    def plot_long_bbands(self, fig, ax, view_limit=500):
        # plot bbands
        # Value of times
        zr = 200 # 200 day lookback for bbands for dca'ing.

        bb_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        bb_df = bb_df.tail(view_limit)

        price = bb_df['Close']

        short_mean = bb_df['Close'].rolling(5).mean() # This is a fine grain filter to catch the absolute lows.
        gld_dth_mean = bb_df['Close'].rolling(50).mean() # For golden and deatch drossovers with 200sma.

        mean = bb_df['Close'].rolling(zr).mean()
        bb_high = mean + 1.96*bb_df['High'].rolling(zr).std()
        bb_low = mean - 1.96*bb_df['Low'].rolling(zr).std()
        # Inner 1 std dev lines, halfway to bbands
        bb_high_1 = mean + 1.0*bb_df['High'].rolling(zr).std()
        bb_low_1 = mean - 1.0*bb_df['Low'].rolling(zr).std()

        # A middle 1.5 stddev set of lines. From testing out hypothesies.
        bb_high_2 = mean + 1.5*bb_df['High'].rolling(zr).std()
        bb_low_2 = mean - 1.5*bb_df['Low'].rolling(zr).std()

        plt.plot(bb_high, label="BB Hi ", color='#FF0000', alpha=0.95,linewidth = 3.5, linestyle = '--')
        plt.plot(bb_low, label="BB Low", color='#FF0000', alpha=0.95,linewidth = 3.5, linestyle = '--')

        # Inner 1 std dev lines, halfway to bbands
        plt.plot(bb_high_1, label="BB Hi 1", color='#FF1010', alpha=0.65,linewidth = 1.5, linestyle = '--')
        plt.plot(bb_low_1, label="BB Low 1", color='#FF1010', alpha=0.65,linewidth = 1.5, linestyle = '--')


        # Inner 1 std dev lines, halfway to bbands
        plt.plot(bb_high_2, label="BB Hi 1,5", color='#FF1080', alpha=0.65,linewidth = 2.25, linestyle = '--')
        plt.plot(bb_low_2, label="BB Low 1.5", color='#FF1080', alpha=0.65,linewidth = 2.25, linestyle = '--')


        plt.plot(mean, label="SMA200", color='red', alpha=0.95,linewidth = 3.5, linestyle = '-')
        plt.plot(price, label="Price", color='#00FF10', alpha=0.95,linewidth  = 2)
        plt.plot(short_mean, label="Short Mean", color='orange', alpha=0.95,linewidth = 2.0)
        #gld_dth_mean = 50SMA.
        plt.plot( gld_dth_mean, label="50SMA Mean", color='green', alpha=0.95,linewidth = 2.0)


        
    # Range generator for decimals
    def drange(self, x, y, jump): 
        while x < y:
            yield float(x)
            x += decimal.Decimal(jump)


IMAGES_PATH = '/tmp'
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

