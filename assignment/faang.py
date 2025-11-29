#!/usr/bin/env -S python3
# The shebang "#!" distinguish it from a standard comment. 
# The "/usr/bin/env python" avoids hard-coding an absolute path to any specific Python interpreter. 
# I'm not sure if my script is backward-compatible with Python 2, so I'm going to explicitly request python3.

# This script will run from github to download stock data for the FAANG stocks from Yahoo Finance

# Course: Computer Infrastructure
# Author: Gerry Callaghan

import yfinance as yf
# This is an open-source package that downloads stock data from Yahoo Finance.

# Dates and times - we will use this package to allow us format dates into strings for filenames.
import datetime as dt


portfolio = ['AAPL', 'AMZN','GOOG', 'META','NFLX']  # FANG stocks

# we specify a five day period (5d) at one hour intervals (1h) as follows
df = yf.download(portfolio, period='5d', interval='1h')


# Let's now print our dataframe out to a CSV file
now = dt.datetime.now()

FILENAME = now.strftime('%Y%m%d-%H%M%S')+'.csv'

# we want to put the csv in a separate folder in the parent directory
DATADIR = "../data/"

# the directory an filename concatenated is then the fullpath
FULLPATH = DATADIR + FILENAME  

# now to print out to this csv
print(df.to_csv(FULLPATH))
