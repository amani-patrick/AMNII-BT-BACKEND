from django.urls import path
from .views import get_accounts, add_account, update_account, delete_account

urlpatterns = [
    path('', get_accounts, name='get_accounts'),
    path('add/', add_account, name='add_account'),
    path('<int:account_id>/update/', update_account, name='update_account'),
   path('<int:account_id>/delete/', delete_account, name='delete_account'),
]
