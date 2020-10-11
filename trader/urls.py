from django.urls import path
from . import views

# back-end router
urlpatterns = [
    path('', views.home, name = 'home-page'),
    path('stock', views.stock, name = 'stock-page'),
    path('portfolio', views.portfolio, name = 'portfolio-page'),
]
