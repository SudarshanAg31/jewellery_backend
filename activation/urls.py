from django.urls import path
from . import views

urlpatterns = [
    path('request-access/', views.request_access),
    path('check-status/', views.check_status),
    path('mark-activated/', views.mark_activated),
]