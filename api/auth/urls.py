from django.urls import path
from api.auth.views import signup, login, logout  
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', signup, name='register'),  # Trailing slash
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]