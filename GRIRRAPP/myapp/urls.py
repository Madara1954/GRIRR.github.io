from django.urls import path, include
from django.shortcuts import redirect
from . import views
from .views import verify_email_code, add_child

urlpatterns = [
    path('', views.login_view, name='login'),
    path('parentDashboard/', views.parent_dashboard, name='parentDashboard'),
    path('employeeDashboard/', views.employee_dashboard, name='employeeDashboard'),
    path('children/add/', views.add_child, name='add_child'),
    path('children/', views.add_child, name='children'), 
    path('add_child/', add_child, name='add_child'),
    path('program_costs/', views.program_costs, name='program_costs'),
    path('baselines/', views.baselines, name='baselines'),
    path('toolkit/', views.toolkit, name='toolkit'),
    path('resources/', views.resources, name='resources'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register'),
    path('verify-email/', views.verify_email_code, name='verify_email_code'),
    path('login/', views.login_view, name='login'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('edit_child/<int:child_id>/', views.edit_child, name='edit_child'),
    path('delete_child/<int:child_id>/', views.delete_child, name='delete_child'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),  
    path('admin/myapp/parent/<int:parent_id>/children/', views.parent_details_view, name='admin_parent_details'),
    path('', lambda request: redirect('login', permanent=True)),
]
