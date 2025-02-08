from django.urls import path
from .views import me_view

urlpatterns = [
    path('api/auth/me', me_view, name='me'),  # This will handle the /api/auth/me request
]
