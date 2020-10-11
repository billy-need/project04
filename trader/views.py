from trader.models import Stock
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .forms import StockForm, TickerForm
from .models import Account, Stock

# Create your views here.
def home(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.userName
    context = { 'username': username, 'balance' : round(balance, 2)}
    return render(request, 'trader/home.html', context)

def ticker(request):
    account = get_object_or_404(Account, pk = 1)
    balance = account.balance
    username = account.userName
    form = TickerForm()
    context = { 'username': username, 'balance' : round(balance, 2), 'form': form}
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
