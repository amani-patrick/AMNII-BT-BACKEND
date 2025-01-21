from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),  # Includes auth URLs
    path('accounts/', include('api.accounts.urls')),
    path('markets/', include('api.markets.urls')),
    path('orders/', include('api.orders.urls')),
    path('bot/', include('api.bot.urls')),
    path('strategies/', include('api.strategies.urls')),
    path('notifications/', include('api.notifications.urls')),
    path('analytics/', include('api.analytics.urls')),
]