#!/usr/bin/env -S python3
# The shebang "#!" distinguish it from a standard comment. 
# The "/usr/bin/env python" avoids hard-coding an absolute path to any specific Python interpreter. 
# I'm not sure if my script is backward-compatible with Python 2, so I'm going to explicitly request python3.

# Problems Notebook

# Course: Computer Infrastructure
# Author: Gerry Callaghan

import yfinance as yf
# Yahoo Finance is not part of the cental python repository 
# but is an open-source package available that can be installed via conda-forge.
# This is where we import the yfinance package to allow us to download stock data.
# print(f"The version of yfinance that you're running is: {yf.__version__}")
# There are known issues with yfinance and the default user-agent, so i need to spoof my user-agent
# You can read more about this issue here:
# url= "https://www.reddit.com/r/learnpython/comments/1kc3miq/yfinance_error_yfratelimiterrortoo_many_requests/"
# Details on how requests from the curl_cffi package can be imported url ="https://pypi.org/project/curl-cffi/"
import curl_cffi.requests as requests
session = requests.Session(impersonate="chrome")

# Dates and times - we will use this package to allow us format dates into strings for filenames.
import datetime as dt

# https://stackoverflow.com/questions/33743394/matplotlib-dateformatter-for-axis-label-not-working
import matplotlib.dates as mdates

# data frames - we will use pandas to handle tabular data imported from Yahoo Finance.
import pandas as pd

# plot graphs - we will use matplotlib to plot graphs.
import matplotlib.pyplot as plt 

# need numpy to create two arrays for chats
import numpy as np

import os

import csv   # to read in csv files


# Problem 1: Data from yfinance

# I want to remove the apostrophe because the tickers command in yfinance do not have apostrophes
# so we create a string of stock tickers separated by spaces
portfolio = ['AAPL', 'AMZN','GOOG', 'META','NFLX']  # FANG stocks
#print(f"{len(portfolio)}")
stocks = portfolio[0]
for stock in portfolio[1:]:
        stocks += (" " + stock)
#print(f"{stocks}\n")

# From here URL= "https://ranaroussi.github.io/yfinance/", 
# it says that for multiple tickers we need only have whitespace between each ticker symbol.
# That is, it takes a single string with spaces between each ticker symbol.
# So, our function looks like this, remember we are passing in our session object to avoid user-agent issues.
tickers = yf.Tickers(stocks, session=session)
#print(tickers.tickers)  # This will print the ticker objects for each of our FANG stocks.
stock_names = str()
i = 0
while i < len(portfolio):
        #displayName = tickers.tickers[portfolio[i]].info['longName']
        stock_names = stock_names + (tickers.tickers[portfolio[i]].info['longName']+", ")
        i+=1


# We download the data from yahoo finance into a dataframe as follows
# According to https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
# we specify a five day period (5d) at one hour intervals (1h) as follows
df = yf.download(portfolio, period='5d', interval='1h', session=session)

#df = yf.download(['META', 'AAPL', 'AMZN', 'NFLX', 'GOOG'], period='5d', interval='1h', session=session)
# in the previous command, we had no comma between the stock tickers, 
# but here in this download function, because they are in a tuple, we do need commas, 
# and each have apostrophes to indicate they are strings
# the function is download(),and we it takes variables, ticker/tickers and period

# let's view our columns
#print(f"{df.head()}\n")
# many of these columns we don't need, so let's create a list of columns we want to drop

 # Instead of hardcoding the list of superfluous columns for our stocks, 
 # # because the number of stocks might change
 # let's create it programmatically where we pull in the stocks listed in our portfolio variable above     
stock = portfolio[0]
potential_drop_cols_list = ()
i = 0

while i < len(portfolio):
        
        column1 = ("High",portfolio[i])
        column2= ("Low",portfolio[i])
        column3=("Open",portfolio[i])
        column4=("Volume",portfolio[i])
        stock=(column1,column2,column3,column4)
        potential_drop_cols_list = potential_drop_cols_list + stock
        i+=1

drop_cols_list = list(potential_drop_cols_list)
print(f"{(drop_cols_list)}\n")

# now let's drop this list of columns from our dataframe
df.drop(columns=drop_cols_list, inplace=True)
#let's view the new columns
#headers = df.columns.tolist()
#print(f"{headers}\n")

# All our prices are closing prices, so let's drop the "closing" prefix from each of our column names
# We create new column names as follows

new_stock_names = ["Apple","Amazon","Google","Meta","Netflix"]
print(f"({new_stock_names})\n")
# now set the column names of our dataframe equal to those column names
df.columns = new_stock_names

headers = df.columns.tolist()
print(f"{headers}\n")

#print(f"{df}\n")


# Let's now print our dataframe out to a CSV file
# we will use the to_csv funtion, you can read about it here https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html

# Before we export it out, we want to give our csv file a name based on today's date

# We assign a new variable today equal to the current date and time
now = dt.datetime.now()

# We format the date and time of today according to a manner we want
# more on this can be found here docs.python.org/3/library/datetime.html#format-codes 
# and docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
print(now.strftime("%Y%m%d-%H%M%S"))

FILENAME = now.strftime('%Y%m%d-%H%M%S')+'.csv'
# we want to put the csv in a separate folder in the parent directory
DATADIR = "../data/"
# the directory an filename concatenated is then the fullpath
FULLPATH = DATADIR + FILENAME  
# now to print out to this csv
print(df.to_csv(FULLPATH))



# Problem 2: Plotting the closing prices.

FILENAME = now.strftime('%Y%m%d-%H%M%S')+'.csv'
DATADIR = "../data/"
FULLPATH = DATADIR + FILENAME   

fp = pd.read_csv(FULLPATH)
new_column_names = ["Date","Apple","Amazon","Google","Meta","Netflix"]
fp.columns = new_column_names 
fp.set_index('Date', inplace=True)
print(f"{fp}")


# We use numpy to create two arrays, one for our dates and the other for our mean daily temperatures
# from https://www.geeksforgeeks.org/python/use-multiple-columns-in-a-matplotlib-legend/
x = np.array(fp.index)
y1 = np.array(fp["Apple"])
y2 = np.array(fp["Amazon"])
y3 = np.array(fp["Google"])
y4 = np.array(fp["Meta"])
y5 = np.array(fp["Netflix"])

date_from = dt.date.today()- dt.timedelta(days=5) 
date_to = dt.date.today()
dates = [dt.timedelta(days=-5),dt.timedelta(days=-4),dt.timedelta(days=-3),dt.timedelta(days=-2),dt.timedelta(days=-1)]

#values=[y1,y2,y3,y4,y5]

#fig, ax = plt.subplots()
#ax.plot(dates,values)

plt.xlabel("Date")
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.xticks.html
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(np.arange(10), rotation=20)
plt.ylabel("Stock Price (USD)")

          
title = "Stock Prices of the Fang Stocks" + str({now.strftime('%Y-%m-%d at %H:%M:%S')})
plt.title(title)

plt.plot(x,y1, label="Apple")
plt.plot(x,y2, label="Amazon")
plt.plot(x,y3, label="Google")
plt.plot(x,y4, label="Meta")
plt.plot(x,y5, label="Netflix")

#plt.legend(("Apple", "Amazon", "Google", "Meta", "Netflix"),("Apple", "Amazon", "Google", "Meta", "Netflix"))
plt.legend(ncol=1,loc='center left', bbox_to_anchor=(1.0, 0.5),fontsize=10, frameon=True, edgecolor='black', facecolor='lightgray',columnspacing=1.5)

plt.show()

# from Gemini AI, we use create a directory as follows
directory_path = "../plots"
try:
    os.mkdir(directory_path)
    print(f"Directory '{directory_path}' created successfully one level up.")
except FileExistsError:
    print(f"Directory '{directory_path}' already exists.")
except OSError as e:
    print(f"Error creating directory: {e}")

# # up one levels to root and then down into plots
filename = (directory_path) + "/" + now.strftime('%Y%m%d-%H%M%S') + "_stock_prices_of_the_fangs_stocks" + ".png"
#print(f"{filename}")

#plt.savefig(filename)


