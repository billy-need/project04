from django import forms
from .models import Stock

class TickerForm(forms.Form):
    symbol = forms.CharField(initial='MSFT');
    shares = forms.IntegerField(initial=10);
    price = forms.IntegerField(initial=25.00);


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'shares', 'price']
