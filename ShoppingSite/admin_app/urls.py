from django.urls import path
from admin_app import views

urlpatterns = [
    path('dashboard/', views.dashboard),
]
