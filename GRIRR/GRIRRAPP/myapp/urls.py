from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('children/', views.children, name='children'),
    path('program-costs/', views.program_costs, name='program_costs'),
    path('baselines/', views.baselines, name='baselines'),
    path('toolkit/', views.toolkit, name='toolkit'),
    path('resources/', views.resources, name='resources'),
    path('login/', views.login_view, name='login'),
]
