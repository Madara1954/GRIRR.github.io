from django.urls import path, include
from django.shortcuts import redirect
from myapp import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('children/', views.children, name='children'),
    path('program_costs/', views.program_costs, name='program_costs'),
    path('baselines/', views.baselines, name='baselines'),
    path('toolkit/', views.toolkit, name='toolkit'),
    path('resources/', views.resources, name='resources'),
    path('', lambda request: redirect('login', permanent=True)),
]
