from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export_logs/', views.export_logs, name='export_logs'),
    path('clear_logs/', views.clear_logs, name='clear_logs'),
]
