import yfinance as yf
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.http.response import HttpResponse, JsonResponse
import json
import os
from django.conf import settings

#print(dir(yf))
#print(help(yf))

# Get current stock information
def getStockData(request):
    tickerSymbol = request.POST['name']

    try:
        stockInfo = yf.Ticker(tickerSymbol).info
        stockDetails = getStockDataDetails(stockInfo)
        resp = json.dumps(stockDetails)
        return HttpResponse(resp)

    except RemoteDataError as e:
        print ('No data found for {}'.format(tickerSymbol))

    except Exception as e:
        print ('No data found for {}'.format(tickerSymbol) + e)

    
def getStockDataDetails(stockInfo):
    return {
        'name': stockInfo['shortName'],
        'symbol': stockInfo['symbol'],
        'price': stockInfo['regularMarketPrice'],
        'close': stockInfo['previousClose'],
        'high': stockInfo['dayHigh'],
        'low': stockInfo['dayLow'],
        'fiftyTwoHigh': stockInfo['fiftyTwoWeekHigh'],
        'fiftyTwoLow': stockInfo['fiftyTwoWeekLow'],
        'volume': stockInfo['volume'],
        'marketCap': stockInfo['marketCap'],
        'logo_url': stockInfo['logo_url']
    }

# Get historical data to draw plot
def stockPlot(ticker):
    stocks = yf.download(ticker, start = "2020-01-01", end = str(datetime.now().strftime('%Y-%m-%d')))
    stocks['Adj Close'].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(ticker + " Price YTD")
    #plt.show()
    IMGDIR= os.path.join(settings.BASE_DIR,'trader\static')   
    print('savefig(' + IMGDIR + '\stock.png)')
    plt.savefig(IMGDIR + '\stock.png')
    plt.close()

def portfolioPlot(stocks):
    stocks['Price'].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Portfolio Value YTD")
    #plt.show()
    IMGDIR= os.path.join(settings.BASE_DIR,'trader\static')   
    print('savefig(' + IMGDIR + '\portfolio.png)')
    plt.savefig(IMGDIR + '\portfolio.png')
    plt.close()