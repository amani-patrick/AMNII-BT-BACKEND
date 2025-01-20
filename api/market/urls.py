from django.urls import path
from .views import get_symbols, get_symbol_data

urlpatterns = [
    path('symbols/', get_symbols, name='get_symbols'),
    path('symbols/<str:symbol>/', get_symbol_data, name='get_symbol_data'),
]
