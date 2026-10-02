from django.contrib import admin
from django.urls import path, include
from activation.views import welcome

urlpatterns = [
    path('', welcome, name='welcome'), 
    path('admin/', admin.site.urls),
    path('api/', include('activation.urls')),
]