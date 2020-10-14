import yfinance as yf
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from django.http.response import HttpResponse
import os
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render




# Get historical information. This will be called by a view
def get_data(ticker, date):
    startDate = date
    endDate = str(datetime.now().strftime('%Y-%m-%d'))

    try:
        stock_data = data.DataReader(ticker, 'yahoo', startDate, endDate)
        adj_close = clean_data(stock_data, 'Adj Close', startDate, endDate)
        print('adj_close=', adj_close)
        create_plot(adj_close, ticker)
        
    except RemoteDataError:
        print('No data found for {}'.format(ticker))

# Get statistical information
def get_stats(stock_data):
    return {
        'last': np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20).mean,
        'long_rolling': stock_data.rolling(window=200).mean
    }

# Clean the data
def clean_data( stock_data, col, startDate, endDate):
    weekdays = pd.date_range( start=startDate, end=endDate)
    clean_data = stock_data[col].reindex( weekdays)
    return clean_data.fillna( method='ffill')

# Create a plot graph
def create_plot( stock_data, ticker):
    stats = get_stats( stock_data)
    print( stats['last'])
    
    # How to plot on graph
    fig, ax = plt.subplots( figsize=(12,8))
    plt.plot( stock_data, label=ticker)
    plt.xlabel('Date')
    plt.ylabel('Adj Close')
    plt.legend()
    plt.title(ticker + ' Price Over Time')
    plt.show()
    IMGDIR = os.path.join(settings.configure.DIR,'trader/static')
    print('savefig(' + IMGDIR + '\my_plot.png)')
    plt.savefig(IMGDIR + '\my_plot.png')
    plt.close(fig); #need this to end the file

# def draw(request):
#     print('draw called')
#     create_plot('FB')
#     return render(request, 'example/home.html')

get_data('MSFT', '2020-09-14') # called from the view
