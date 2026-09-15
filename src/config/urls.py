
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.smart_search.urls')),
    path('navigate/', include('apps.navigation.urls')),
    path('', include('apps.account.urls')),
]
