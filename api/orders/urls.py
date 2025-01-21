from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.list_orders, name='list_orders'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<str:order_id>/', views.retrieve_order, name='retrieve_order'),
    path('orders/<str:order_id>/update/', views.update_order, name='update_order'),
    path('orders/<str:order_id>/delete/', views.delete_order, name='delete_order'),
]
