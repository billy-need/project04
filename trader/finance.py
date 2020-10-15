import yfinance as yf
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from django.http.response import HttpResponse
import json

#print(dir(yf))
#print(help(yf))

# Get current stock information
def getStock(request):
    tickerSymbol = request.POST['name']
    stockInfo = yf.Ticker(tickerSymbol).info
    stockDetails = getStockDetails(stockInfo)
    resp = json.dumps(stockDetails)
    return HttpResponse(resp)

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

# Get historical stock information