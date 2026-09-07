from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('create', views.employee_create, name='employee_create'),
    path('add/', views.employee_create, name='employee_create'),
    path('edit/<uuid:emp_uuid>/', views.employee_edit, name='employee_edit'),
    path('delete/<uuid:emp_uuid>/', views.employee_delete, name='employee_delete'),
]
