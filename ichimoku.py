# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import numpy as np
import decimal


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
        last_date = ohcl_df["Date"].iloc[-1]
        period = last_date - ohcl_df["Date"].iloc[-2]

        # Add rows for N periods shift (cloud_displacement)
        ext_beginning = decimal.Decimal(last_date+period)
        ext_end = decimal.Decimal(last_date + ((period*cloud_displacement)+period))
        dates_ext = list(self.drange(ext_beginning, ext_end, str(period)))
        dates_ext_df = pd.DataFrame({"Date": dates_ext})
        dates_ext_df.index = dates_ext # also update the df index
        ohcl_df = ohcl_df.append(dates_ext_df)

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

    def plot(self):
        fig, ax = plt.subplots()    
        self.plot_candlesticks(fig, ax)
        self.plot_ichimoku(fig, ax)
        self.pretty_plot(fig, ax)
        plt.show()

    def pretty_plot(self, fig, ax):
        ax.legend()
        fig.autofmt_xdate()
        ax.xaxis_date()

        # Chart info
        title = 'Ichimoku Demo (XRP/BTC)'
        bgcolor = '#131722'
        grid_color = '#363c4e'
        spines_color = '#d9d9d9'
        # Axes
        plt.title(title, color='white')
        plt.xlabel('Date', color=spines_color, fontsize=7)
        plt.ylabel('Price (BTC)', color=spines_color, fontsize=7)

        ax.set_facecolor(bgcolor)
        ax.grid(linestyle='-', linewidth='0.5', color=grid_color)
        ax.yaxis.tick_right()
        ax.set_yscale("log", nonposy='clip')
        fig.patch.set_facecolor(bgcolor)
        fig.patch.set_edgecolor(bgcolor)
        plt.rcParams['figure.facecolor'] = bgcolor
        plt.rcParams['savefig.facecolor'] = bgcolor
        ax.spines['bottom'].set_color(spines_color)
        ax.spines['top'].set_color(spines_color) 
        ax.spines['right'].set_color(spines_color)
        ax.spines['left'].set_color(spines_color)
        ax.tick_params(axis='x', colors=spines_color, size=7)
        ax.tick_params(axis='y', colors=spines_color, size=7)
        fig.tight_layout()
        ax.autoscale_view()

    def plot_ichimoku(self, fig, ax, view_limit=100):
        d2 = self.ohcl_df.loc[:, ['tenkan_sen','kijun_sen','senkou_span_a','senkou_span_b', 'chikou_span']]
        d2 = d2.tail(view_limit)
        date_axis = d2.index.values
        # ichimoku
        plt.plot(date_axis, d2['tenkan_sen'], label="tenkan", color='#0496ff', alpha=0.65,linewidth=0.5)
        plt.plot(date_axis, d2['kijun_sen'], label="kijun", color="#991515", alpha=0.65,linewidth=0.5)
        plt.plot(date_axis, d2['senkou_span_a'], label="span a", color="#008000", alpha=0.65,linewidth=0.5)
        plt.plot(date_axis, d2['senkou_span_b'], label="span b", color="#ff0000", alpha=0.65, linewidth=0.5)
        plt.plot(date_axis, d2['chikou_span'], label="chikou", color="#ffffff", alpha=0.65, linewidth=0.5)
        # green cloud
        ax.fill_between(date_axis, d2['senkou_span_a'], d2['senkou_span_b'], where=d2['senkou_span_a']> d2['senkou_span_b'], facecolor='#008000', interpolate=True, alpha=0.25)
        # red cloud
        ax.fill_between(date_axis, d2['senkou_span_a'], d2['senkou_span_b'], where=d2['senkou_span_b']> d2['senkou_span_a'], facecolor='#ff0000', interpolate=True, alpha=0.25)

    def plot_candlesticks(self, fig, ax, view_limit=100):
        # plot candlesticks
        candlesticks_df = self.ohcl_df.loc[:, ['Date','Open','High','Low', 'Close']]
        candlesticks_df = candlesticks_df.tail(view_limit)
        # plot candlesticks
        candlestick_ohlc(ax, candlesticks_df.values, width=0.6, colorup='#83b987', colordown='#eb4d5c', alpha=0.5 )

    # Range generator for decimals
    def drange(self, x, y, jump): 
        while x < y:
            yield float(x)
            x += decimal.Decimal(jump)