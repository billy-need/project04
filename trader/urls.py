from django.urls import path
from . import views
from . import finance
from django.conf import settings
from django.conf.urls.static import static

# back-end router
urlpatterns = [
    path('', views.home),
    path('portfolio', views.portfolio),
    path('findstock', finance.getStock),
    path('transactions', views.getTransactions),
    path('buystock', views.buyStock),
    path('sellstock', views.sellStock),
    path('login', views.login_view),
    path('logout', views.logout_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
