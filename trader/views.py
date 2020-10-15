from django.http import request
from django.http.response import HttpResponse
from trader.models import Stock
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .forms import StockForm, TickerForm
from .models import Account, Stock
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
import json

# Create your views here.
def home(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.username
    tickerForm = TickerForm()
    # portfolio = Stock.objects.all()
    transactions = getTransactions()
    context = { 'username': username, 'balance' : round(balance, 2), 'tickerForm' : tickerForm, 'transactions' : transactions}
    return render(request, 'trader/home.html', context)

def buyStock(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    if request.method == "POST":
        data = json.loads(request.body)
        print("Json=" + str(data))
        symbol = data['symbol']
        shares = data['shares']
        price = data['price']
        if account.balance >= int(float(price)) * int(float(shares)):
            account.balance = balance - int(float(price)) * int(float(shares))
            account.save();
            Stock.objects.create(symbol=symbol, shares=shares, price=price)
        else:
            print('Error: Insufficent Funds') # create an error message screen
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")
           
def sellStock(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    if request.method == "POST":
        data = json.loads(request.body)
        print("Json=" + str(data))
        symbol = data['symbol']
        shares = data['shares']
        price = data['price']
        stocks = Stock.objects.filter(symbol=symbol)
        for stock in stocks:
            if stock.shares > shares:
                account.balance = balance + (float(price) * float(shares))
                stock.shares = stock.shares - shares
                stock.save()
            elif stock.shares == shares:
                account.balance = balance + (float(price) * float(shares))            
                stock.delete()
            else:
                print('Error: Cannot sell more than you own')
    account.save();
    getTransactions();
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")
        
def getTransactions():
    transactions = Stock.objects.all()
    return transactions

def portfolio(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.username
    portfolio = Stock.objects.all()
    context = { 'portfolio': portfolio, 'username': username, 'balance' : round(balance, 2)}
    return render(request, 'trader/portfolio.html', context)

def login_view(request):
    user = authenticate(request, username='root', password='password123')
    if user is not None:
        print('username is authenticated')
        login(request, user)
        return redirect('/')

def logout_view(request):
    logout(request)
    return redirect ('/')

    