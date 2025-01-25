from django.urls import path
from . import views  

urlpatterns = [
    path('forex/<str:symbol>/', views.get_forex_data, name='get_forex_data'),
]
