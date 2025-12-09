#!/usr/bin/env -S python3
# The shebang "#!" distinguish it from a standard comment. 
# The "/usr/bin/env python" avoids hard-coding an absolute path to any specific Python interpreter. 
# I'm not sure if my script is backward-compatible with Python 2, so I'm going to explicitly request python3.
# This will allow me to run the script from elsewhere by just calling ./faang.py

# This script will run from github to download stock data for the FAANG stocks from Yahoo Finance

# Course: Computer Infrastructure
# Author: Gerry Callaghan

# External libraries or packages I use in this project

# dates and times - among other things, I use this package to format dates into strings for that i can append to filenames.
import datetime as dt

# data frames - I use pandas to handle tabular data imported from yFinance's csv file.
import pandas as pd

# need numpy to create arrays for charts
import numpy as np

# plot graphs - I use matplotlib to plot graphs of the stocks.
import matplotlib.pyplot as plt 

# Yahoo Finance is not part of the cental python repository but is an open-source package available that can be installed via conda-forge.
# This open-source library that provides a reliable, threaded, and pythonic way to download historical market data from Yahoo! Finance.
import yfinance as yf
# I had issues with older versions of yfinance, so I want to confirm the version I'm using. This will also help with debugging if I encounter any issues.
print(yf.__version__)

# There are known issues with yfinance and the default user-agent, so i need to spoof my user-agent
# You can read more about this issue here: https://www.reddit.com/r/learnpython/comments/1kc3miq/yfinance_error_yfratelimiterrortoo_many_requests/
# Details on how requests from the curl_cffi package can be imported can be found here: https://pypi.org/project/curl-cffi/
import curl_cffi.requests as requests
# this will tell Yahoo Finance that my useragent string is a Chrome Browser because apparently this browser was more dependable for access Yahoo Finance
session = requests.Session(impersonate="chrome")

# this is needed to handle file paths
import os

# to read in csv files
import csv 

# **************** User-Defined Variables ********************************************************
# Collate information over the last five days
days_of_data = "5d"

# Collate hourly prices
frequency_of_prices="1h"

# My stock tickers
stock_tickers = ['AAPL', 'AMZN','GOOG', 'META','NFLX']  # Here I am specifying the FAANG stocks to be downloaded
# **************************************************************************************

def get_data(stock_tickers,days_of_data,frequency_of_prices):
    
    # Download the data from yahoo finance into a dataframe as follows, specifying a period (5 days) at a particular intervals (1 hour )
    df = yf.download(stock_tickers, period=days_of_data, interval=frequency_of_prices, session=session)

    # We assign a new variable "now" equal to the current date and time
    now = dt.datetime.now()

    # Format the "now" variable to YYYYMMDD-HHMMSS
    print(now.strftime("%Y%m%d-%H%M%S"))

    # Assigning the variable FILENAME the value of the now variable plus the .csv suffix
    FILENAME = now.strftime('%Y%m%d-%H%M%S')+'.csv'

    # Assign a variable the path to save the csv files, 
    # As script is run from Github, I don't need the two dots 
    DATADIR = "data/"

    # the directory and filename concatenated is then the fullpath
    FULLPATH = DATADIR + FILENAME  

    # now to print out to this csv
    print(df.to_csv(FULLPATH))
  

# I'm going to call my function to download the data and export to csv
get_data(stock_tickers,days_of_data,frequency_of_prices)


def plot_data():

    # Assign a variable the path containing the csv files, 
    # As script is run from Github, I don't need the two dots 
    DATADIR = "data/"

    # list files in the data folder
    data_files = os.listdir(DATADIR)

    # sort the list of files in chronological order, latest first
    data_files.sort(reverse=True)

    # the latest file will now be the first in the sorted list, so array position 0
    FILENAME = data_files[0]

    # the directory and filename concatenated is then the fullpath
    FULLPATH = DATADIR + FILENAME  

    # Read in the csv file 
    df= pd.read_csv(FULLPATH, header=[0,1], index_col=0, parse_dates=True)
     
    # Create new figure and axis objects
    fig, ax = plt.subplots()

    # Referencing the word "Close", Pandas shows the column names containing that word
    df["Close"].plot(ax=ax)

    # Assign names to be x and y axis
    plt.xlabel("Date",rotation=10)
    plt.ylabel("Stock Price (USD)")

    # Add the current date and time to the title of my plot
    now = dt.datetime.now()
    title = "Stock Prices of the Fang Stocks" + str({now.strftime('%Y-%m-%d at %H:%M:%S')})
    plt.title(title)

    # Format the legend
    plt.legend(ncol=1,loc='center left', bbox_to_anchor=(0.75, 0.75),fontsize=10, frameon=True, edgecolor='black', facecolor='lightgray',columnspacing=1.5)

    # Save the plot in a plots folder
    # As script is run from Github, I don't need the two dots prefix
    directory_path = "plots"

    # Create the plots directory if it doesn't exist
    try:
        os.mkdir(directory_path)
        print(f"Directory '{directory_path}' created successfully one level up.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except OSError as e:
        print(f"Error creating directory: {e}")

    # Assign a variable the concatenation of the path and filename 
    filename = (directory_path) + "/" + now.strftime('%Y%m%d-%H%M%S') + "_stock_prices_of_the_fangs_stocks" + ".png"

    # Now to save the chart to that file. 
    fig.savefig(filename, dpi=300)

# I'm going to call my function to import the data from the latest csv and saves the plots to a plots folder
plot_data() 