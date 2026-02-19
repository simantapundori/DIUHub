from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('mark/<int:registration_id>/', views.mark_attendance, name='mark_attendance'),
]