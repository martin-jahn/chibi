from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('secret/admin/', admin.site.urls),
    path('', include('apps.chibi.urls')),
]
