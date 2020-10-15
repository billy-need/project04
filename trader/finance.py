import yfinance as yf
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.http.response import HttpResponse
import json
import os
from django.conf import settings

#print(dir(yf))
#print(help(yf))

# Get current stock information
def getStock(request):
    tickerSymbol = request.POST['name']

    try:
        stockInfo = yf.Ticker(tickerSymbol).info
        stockDetails = getStockDetails(stockInfo)
        resp = json.dumps(stockDetails)
        return HttpResponse(resp)

    except RemoteDataError:
        print ('No data found for {}'.format(tickerSymbol))

    
def getStockDetails(stockInfo):
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
def createPlot(ticker):
    newtime = yf.download(ticker, start = "2020-01-01", end = str(datetime.now().strftime('%Y-%m-%d')))
    newtime['Adj Close'].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(ticker + " Price YTD")
    #plt.show()
    IMGDIR= os.path.join(settings.BASE_DIR,'trader\static')   
    print('savefig(' + IMGDIR + '\stock.png)')
    plt.savefig(IMGDIR + '\stock.png')
    plt.close()