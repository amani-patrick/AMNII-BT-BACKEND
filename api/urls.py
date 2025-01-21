from django.urls import include, path

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('accounts/', include('api.accounts.urls')),
    path('market/', include('api.markets.urls')),
    path('orders/', include('api.orders.urls')),
    path('bot/', include('api.bot.urls')),
    path('strategies/', include('api.strategies.urls')),
    path('notifications/', include('api.notifications.urls')),
    path('analytics/', include('api.analytics.urls')),
]
