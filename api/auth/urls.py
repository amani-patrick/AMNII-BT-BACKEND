from django.urls import path
from api.auth.views import signup, login, logout,refresh_token

from .views import signup

urlpatterns = [
    path('register/', signup, name='register'), 
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('token/refresh/',refresh_token , name='token_refresh'),

]