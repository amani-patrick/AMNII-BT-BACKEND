from django.urls import path
from .views import user_me

urlpatterns = [
    path('me/',user_me, name='me'),  # This will handle the /api/auth/me request
]
