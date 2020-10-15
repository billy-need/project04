from django import forms
from .models import Stock

class TickerForm(forms.Form):
    symbol = forms.CharField(widget=forms.TextInput(
        attrs= {'id' : 'stockInput', 'placeholder' : 'Symbol...'}
    ))
    # symbol = forms.CharField(initial='MSFT');
    # shares = forms.IntegerField(initial=10);
    # price = forms.IntegerField(initial=25.00);


class MyAjaxForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs= {'id' : 'name', 'placeholder' : 'Enter a name'}
    )) 

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'shares', 'price']
