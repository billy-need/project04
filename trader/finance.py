import yfinance as yf
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from django.http.response import HttpResponse, JsonResponse
import json
import os
from django.conf import settings
from decimal import Decimal

#print(dir(yf))
#print(help(yf))

def getStockData(tickerSymbol):
    try:
        stockInfo = yf.Ticker(tickerSymbol).info
        stockPlot(tickerSymbol)
        today = Decimal(stockInfo['previousClose'] - stockInfo['regularMarketPrice']).quantize(Decimal("0.01"))
        return {
            'name': stockInfo['shortName'],
            'symbol': stockInfo['symbol'],
            'price': stockInfo['regularMarketPrice'],
            'today': today,
            'close': stockInfo['previousClose'],
            'high': stockInfo['dayHigh'],
            'low': stockInfo['dayLow'],
            'fiftyTwoHigh': stockInfo['fiftyTwoWeekHigh'],
            'fiftyTwoLow': stockInfo['fiftyTwoWeekLow'],
            'volume': stockInfo['volume'],
            'marketCap': stockInfo['marketCap'],
            'logo_url': stockInfo['logo_url']
        }


    except RemoteDataError as e:
        print ('No data found for {}'.format(tickerSymbol))

    except Exception as e:
        print ('No data found for heres exception {}'.format(tickerSymbol) + str(e))


# tday = datetime.date.today()
# print(tday.weekday()) #Mon 0 Sun 6
# print(tday.isoweekday()) # Mon 1 Sun 7
# year = (tday.day)
# month = (tday.month)
# day = (tday.day)
# tdelta = datetime.timedelta(days=7)
# oneWeek = tday + tdelta


#startDate = datetime.date(date)



# Get historical data to draw plot
def stockPlot(ticker):
    ticker = ticker.upper()
    stocks = yf.download(ticker, start = '2020-01-01', end = str(datetime.now().strftime('%Y-%m-%d')))
    stocks['Adj Close'].plot()
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xlabel("Date").set_color("white")
    plt.ylabel("Price").set_color("white")
    plt.title(ticker + " Price YTD")
    IMGDIR= os.path.join(settings.BASE_DIR,'trader\static')   
    print('savefig(' + IMGDIR + '\stock.png)')
    plt.savefig(IMGDIR + '\stock.png', transparent=True)
    plt.close()

def portfolioPlot(stocks):
    stocks['Price'].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Portfolio Value YTD")
    IMGDIR= os.path.join(settings.BASE_DIR,'trader\static')   
    print('savefig(' + IMGDIR + '\portfolio.png)')
    plt.savefig(IMGDIR + '\portfolio.png')
    plt.close()