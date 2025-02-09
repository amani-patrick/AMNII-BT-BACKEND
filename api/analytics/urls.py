from django.urls import path
from .views import get_analytics, get_symbol_analytics

urlpatterns = [
    path('', get_analytics, name='get_analytics'), 
    path('<str:symbol>/', get_symbol_analytics, name='symbol_analytics'), 
]
