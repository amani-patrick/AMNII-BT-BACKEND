from django.urls import path
from .views import get_accounts, add_account, update_account, delete_account

urlpatterns = [
    path('', get_accounts, name='get_accounts'),
    path('add/', add_account, name='add_account'),
    path('<str:account_name>/update/', update_account, name='update_account'),  # Use account_name for update
    path('<str:account_name>/delete/', delete_account, name='delete_account'),  # Use account_name for delete
]
