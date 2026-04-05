from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),

    # QR scan (NEW)
    path('scan/', views.scan_qr, name='scan_qr'),

    # manual fallback 
    path('mark/<int:registration_id>/', views.mark_attendance, name='mark_attendance'),
]