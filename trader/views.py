from django.http import request
from django.http.response import HttpResponse
from trader.models import Stock
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .forms import StockForm, TickerForm
from .models import Account, Stock
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

# Create your views here.
def home(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.userName
    tickerForm = TickerForm()
    context = { 'username': username, 'balance' : round(balance, 2), 'tickerForm' : tickerForm}
    return render(request, 'trader/home.html', context)

def stock(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.userName
    stocks = get_list_or_404(Stock)
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid(): # look up error codes for is_valid
            price = form.cleaned_data['price']
            symbol = form.cleaned_data['symbol']
            shares = form.cleaned_data['shares']
            action = request.POST['submit']
            if action == "Buy":
                if account.balance >= price * shares:
                    account.balance = balance - (price * shares)
                    form.save();
                else:
                    print('Error: Insufficent Funds') # create an error message screen
            if action == "Sell":
                # account.balance = balance + (price * shares)
                for stock in stocks:
                    if stock.symbol == symbol:
                        if stock.shares > shares:
                            account.balance = balance + (price * shares)
                            stock.shares = stock.shares - shares
                            stock.save()
                        if stock.shares == shares:
                            account.balance = balance + (price * shares)
                            stock.delete()
                        else:
                            print('Error: Cannot sell more than you own')
                        break 
                    else:
                        print('Error: Cannot find stock symbol')
            account.save();
            return redirect('/stock')
    form = StockForm()
    context = { 'form': form, 'username': username, 'balance' : round(balance, 2)}
    return render(request, 'trader/stock.html', context)

def portfolio(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.userName
    portfolio = Stock.objects.all()
    context = { 'portfolio': portfolio, 'username': username, 'balance' : round(balance, 2)}
    return render(request, 'trader/portfolio.html', context)

def login_view(request):
    user = authenticate(request, username='root', password='password123')
    if user is not None:
        print('username is authenticated')
        login(request, user)
        return redirect('/home2')

def logout_view(request):
    logout(request)
    return redirect ('/home2')