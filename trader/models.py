from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=25);
    password = models.CharField(max_length=25);
    balance = models.DecimalField(max_digits=20, decimal_places=4);
    def __str__(self):
        return "userName=" + str(self.userName) + ", password=" + str(self.password) + ", balance=" + str(self.balance);

class Stock(models.Model):
    symbol = models.CharField(max_length=5);
    shares = models.IntegerField(); # entered by user
    price = models.DecimalField(max_digits=10, decimal_places=2) # calculated from info on finance
    orderDate = models.DateTimeField(auto_now_add=True);