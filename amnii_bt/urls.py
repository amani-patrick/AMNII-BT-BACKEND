from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import redirect
from django.http import JsonResponse


def root_redirect(request):
    """Redirect root URL to the API documentation."""
    return redirect('/api/')
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('health/', health_check, name='health_check'),
    path('docs/', include('rest_framework_swagger.urls')),  
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
