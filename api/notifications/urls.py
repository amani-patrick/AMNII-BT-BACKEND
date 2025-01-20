from django.urls import path
from .views import get_notifications, create_notification

urlpatterns = [
    path('', get_notifications, name='get_notifications'),
    path('create/', create_notification, name='create_notification'),
]
