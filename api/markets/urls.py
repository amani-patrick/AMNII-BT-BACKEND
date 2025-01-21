from django.urls import path
from . import views  # Import views from the same directory

urlpatterns = [
    path('forex/<str:symbol>/', views.get_forex_data, name='get_forex_data'),
]
