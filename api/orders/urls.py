from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_retrieve, name='order_retrieve'),
    path('<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('<int:pk>/tp_sl/', views.order_update_tp_sl, name='order_update_tp_sl'),
    path('<int:pk>/pnl/', views.order_update_pnl, name='order_update_pnl'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('netprofit/',views.net_profit, name='net_profit'),
]
