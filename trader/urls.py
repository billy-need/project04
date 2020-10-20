from django.urls import path
from . import views
from . import finance
from .models import Transaction
from django.conf import settings
from django.conf.urls.static import static

# back-end router
urlpatterns = [
    path('', views.home),
    path('portfolio', views.portfolio),
    path('account', views.account),
    path('getstock', views.home),
    #path('ajax/getStockData', views.getStockData)
    path('transactions', Transaction.getTransactions),
    path('buystock', views.buyStock),
    path('sellstock', views.sellStock),
    path('resetaccount', views.resetAccount),
    path('login', views.login_view),
    path('logout', views.logout_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)