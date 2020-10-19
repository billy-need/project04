from typing import cast
from django.http import request
from django.http.response import *
from trader.models import Stock
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .forms import StockForm, TickerForm
from .models import Account, Stock, Transaction
from .finance import stockPlot, portfolioPlot
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
import json

# Create your views here.
def home(request):
    account = Account.getAccount(1)
    balance = account.balance
    username = account.username
    transactions = Transaction.getTransactions()
    context = {'username': username, 'balance': round(balance, 2), 'transactions': transactions}
    return render(request, 'trader/home.html', context)

def drawGraph(request): #multi thread bug!!!
    tickerSymbol = request.POST['name']
    stockPlot(tickerSymbol)
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")

def portfolio(request):  #needs work
    account = Account.getAccount(1)
    balance = account.balance
    username = account.username
    transactions = Transaction.getTransactions()
    # portfolioPlot(transactions)
    context = {'username': username, 'balance': round(balance, 2), 'transactions': transactions}
    return render(request, 'trader/portfolio.html', context)

def account(request):
    account = Account.getAccount(1)
    balance = account.balance
    username = account.username
    password = account.password
    context = {'username': username, 'password': password, 'balance': round(balance, 2)}
    return render(request, 'trader/account.html', context)

def resetAccount(userId = 1):
    Account.resetBalance(userId)
    Stock.deleteAllStock()
    Transaction.deleteAllTransactions()
    return redirect('/account')


def buyStock(request):
    account = Account.getAccount(1)
    balance = account.balance

    try:
        if request.method == "POST":
            data = json.loads(request.body)
            print("Json=" + str(data))
            symbol = data['symbol']
            name = data['name']
            shares = data['shares']
            price = data['price']
            if balance >= int(float(price)) * int(float(shares)):
                account.balance = balance - int(float(price)) * int(float(shares))
                account.save()
                Stock.createStock(symbol, name, shares, accountId = 1)
                Transaction.createTransaction('buy', symbol, shares, price, accountId = 1)
            else:
                print(str('Error: Insufficent Funds'))  # create an error message screen
        return HttpResponseRedirect('/')
    
    except Exception as e:
        print(str(e))
        return HttpResponseBadRequest(e)

def sellStock(request):
    account = Account.getAccount(1)
    balance = account.balance

    try:
        if request.method == "POST":
            data = json.loads(request.body)
            print("Json=" + str(data))
            symbol = data['symbol']
            shares = data['shares']
            price = data['price']
            Stock.deleteStock(symbol, shares)
            account.balance = balance + int((float(price)) * int(float(shares)))
            account.save()
        return HttpResponseRedirect('/')

    except Exception as e:
        print(str(e))
        return HttpResponseBadRequest(e)


def login_view(request):
    user = authenticate(request, username='root', password='password123')
    if user is not None:
        print('username is authenticated')
        login(request, user)
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')
