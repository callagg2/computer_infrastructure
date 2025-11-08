#!/usr/bin/env -S python3

# Problems Notebook

# Course: Computer Infrastructure
# Author: Gerry Callaghan

# Problem 1: Data from yfinance

# The shebang "#!" distinguish it from a standard comment. The "/usr/bin/env python" avoids hard-coding an absolute path to any specific Python interpreter. I'm not sure if my script is backward-compatible with Python 2, so I'm going to explicitly request python3.

import yfinance
print(f"The version of yfinance that you're running is: {yfinance.__version__}")

# Dates and times - we will use this package to allow us format dates into strings for filenames.
import datetime as dt

# data frames - we will use pandas to handle tabular data imported from Yahoo Finance.
import pandas as pd

# plot graphs - we will use matplotlib to plot graphs.
import matplotlib.pyplot as plt 

# need numpy to create two arrays for chats
import numpy as np

# Yahoo Finance is not part of the cental python repository 
# but is an open-source package available that can be installed via conda-forge.
# This is where we import the yfinance package to allow us to download stock data.
import yfinance as yf


# There are known issues with yfinance and the default user-agent, so i need to spoof my user-agent
# You can read more about this issue here:
# url= "https://www.reddit.com/r/learnpython/comments/1kc3miq/yfinance_error_yfratelimiterrortoo_many_requests/"
# Details on how requests from the curl_cffi package can be imported url ="https://pypi.org/project/curl-cffi/"
import curl_cffi.requests as requests
session = requests.Session(impersonate="chrome")

# From here URL= "https://ranaroussi.github.io/yfinance/", 
# it says that for multiple tickers we need only have whitespace between each ticker symbol.
# That is, it takes a single string with spaces between each ticker symbol.
# So, our function looks like this, remember we are passing in our session object to avoid user-agent issues.
tickers = yf.Tickers('META AAPL AMZN NFLX GOOG', session=session)
print(tickers.tickers)  # This will print the ticker objects for each of our FANG stocks.

df = yf.download(['META', 'AAPL', 'AMZN', 'NFLX', 'GOOG'], period='5d', interval='1h', session=session)

#in the previous command, we had no comma between the stock tickers, 
#but here, because they are in a tuple, we do, and each have apostrophes to indicate they are strings
# the function is download(),and we it takes variables, ticker/tickers and period

# What is the period, 5 days in our case. From URL= "https://algotrading101.com/learn/yfinance-guide/" 5 days is '5d', 
# while we want hourly data, so we set interval='1h' for 1 hour intervals.
#df

# details of this function can be found here https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
# it says the format of the command is
# yfinance.download(tickers, start=None, end=None, actions=False, threads=True, ignore_tz=None, group_by='column', auto_adjust=None, 
# back_adjust=False, repair=False, keepna=False, progress=True, period=None, interval='1d', prepost=False, proxy=<object object>, 
# rounding=False, timeout=10, session=None, multi_level_index=True) 

# We want to have a copy of the data, copy it to a dataframe called df

# let's confirm the type of dataframe we have
type(df)

# print data as CSV file
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
print(df.to_csv('../data/data.csv'))

# Dates and Times

# Current date and time
now = dt.datetime.now()
# docs.python.org/3/library/datetime.html#format-codes 
print(f"{now}")

# Format date and time
print(now.strftime("%Y-%m-%d %H:%M:%S"))
# docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
print(now.strftime("%Y%m%d-%H%M%S"))

# File name
"../data/" + now.strftime('%Y%m%d-%H%M%S')+'.csv'

# print(df.to_csv("../data/" + now.strftime('%Y%m%d-%H%M%S')+'.csv'))
print(df.to_csv("../data/" + dt.datetime.now().strftime('%Y%m%d-%H%M%S')+'.csv'))

df.columns
drop_cols_list = [(  'High', 'AAPL'),
            (  'High', 'AMZN'),
            (  'High', 'GOOG'),
            (  'High', 'META'),
            (  'High', 'NFLX'),
            (   'Low', 'AAPL'),
            (   'Low', 'AMZN'),
            (   'Low', 'GOOG'),
            (   'Low', 'META'),
            (   'Low', 'NFLX'),
            (  'Open', 'AAPL'),
            (  'Open', 'AMZN'),
            (  'Open', 'GOOG'),
            (  'Open', 'META'),
            (  'Open', 'NFLX'),
            ('Volume', 'AAPL'),
            ('Volume', 'AMZN'),
            ('Volume', 'GOOG'),
            ('Volume', 'META'),
            ('Volume', 'NFLX')]
df.drop(columns=drop_cols_list, inplace=True)
headers = df.columns.tolist()
print(f"{headers}\n")

df.index
# this tells us all the values for the x-axis, which is date and time stamps

# Problem 2: Plotting Data
'''
df[('Close','META')].plot()
#so this plot the closing price for MSFT for one month (October 2025)
'''

# Plotting the closing prices.

# We use numpy to create two arrays, one for our dates and the other for our mean daily temperatures
x = np.array(df.index)
y = np.array(df)

plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title("Stock Prices of the Fang Stocks {now.strftime('%Y%m%d-%H%M%S')}")

plt.plot(x,y)
#plt.show()

# # up one levels to root and then down into plots
datadir = "../plots/"
filename = datadir + "{now.strftime('%Y%m%d-%H%M%S')}_stock_prices_of_the_fangs_stocks.png"
print(f"{datadir + filename}")
#open(people_filename)

plt.savefig(filename)
