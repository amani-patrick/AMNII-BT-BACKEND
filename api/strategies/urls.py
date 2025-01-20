from django.urls import path
from .views import get_strategies, create_strategy

urlpatterns = [
    path('', get_strategies, name='get_strategies'),
    path('create/', create_strategy, name='create_strategy'),
]
