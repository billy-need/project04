import yfinance as yf
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from django.http.response import HttpResponse

#print(dir(yf))
#print(help(yf))

# ticker = 'TSLA'
# stock = yf.download(ticker, start=startDate, end=endDate)
# print(stock.head(5))


# to get current informatoin
def getStockName(request):
    tickerSymbol = request.POST['name']
    tickerData = yf.Ticker(tickerSymbol)
    tickerInfo = tickerData.info
    stockName = tickerInfo['shortName']
    print('Found stock name: ' + stockName)
    return HttpResponse(stockName)

#getStockName('MSFT')
# startDate = '2012-01-01'
# endDate = str(datetime.now().strftime('%Y-%m-%d'))
# print('endDate= ', endDate)


# def get_stats(stock_data):
#     return {
#         'last': np.mean(stock_data.tail(1)),
#         'short_mean': np.mean(stock_data.tail(20)),
#         'long_mean': np.mean(stock_data.tail(200)),
#         'short_rolling': stock_data.rolling(window=20),
#         'long_rolling': stock_data.rolling(window=200)
#     }

# def clean_data( stock_data, col):
#     weekdays = pd.date_range( start=startDate, end=endDate)
#     clean_data = stock_data[col].reindex( weekdays)
#     return clean_data.fillna( method='ffill')

# def create_plot( stock_data, ticker):
#     stats = get_stats( stock_data)
#     print( stats['last'])
    
#     # How to plot on graph
#     fig, ax = plt.subplots( figsize=(12,8))
#     plt.plot( stock_data, label=ticker)
#     plt.xlabel('Date')
#     plt.ylabel('Adj Close')
#     plt.legend();
#     plt.title('Stock Price over Time')
#     #plt.show();
#     fig.savefig('stock.png')
#     plt.close(fig); #need this to end the file


# # To get historical information. This will be called by a view
# def get_data(ticker):
#     try:
#         stock_data = data.DataReader(ticker, 'yahoo', startDate, endDate)
#         adj_close = clean_data(stock_data, 'Adj Close')
#         print('adj_close=', adj_close)
#         create_plot(adj_close, ticker)
        
#     except RemoteDataError:
#         print('No data found for {}'.format(ticker))

# get_data('TSLA')

