from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),

    path('projects/<int:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
]