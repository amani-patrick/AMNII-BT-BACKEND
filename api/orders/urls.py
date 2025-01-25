from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_retrieve, name='order_retrieve'),
    path('orders/<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('orders/<int:pk>/tp_sl/', views.order_update_take_profit_stop_loss, name='order_update_tp_sl'),
    path('orders/<int:pk>/pnl/', views.order_update_pnL, name='order_update_pnl'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
]
