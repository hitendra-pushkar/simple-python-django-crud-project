from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.student_list, name='student_list'),
    path('add/', views.student_add, name='student_add'),
    path('edit/<uuid:student_uuid>/', views.student_edit, name='student_edit'),
    path('delete/<uuid:student_uuid>', views.student_delete, name='student_delete')
]