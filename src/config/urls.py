
from django.contrib import admin
from django.urls import path,include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('apps.smart_search.urls')),

    path('navigate/', include('apps.navigation.urls')),

    path('', include('apps.account.urls')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
