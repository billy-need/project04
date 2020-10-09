from django.urls import path
from . import views

# back-end router
urlpatterns = [
    path('', views.home, name = 'home-page')
]
