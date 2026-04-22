from django.urls import path
from . import views

urlpatterns = [
    # 📊 Attendance List
    path('', views.attendance_list, name='attendance_list'),

    # 📷 QR Scan (ADMIN ONLY)
    path('scan/', views.scan_qr, name='scan_qr'),
    path('report/', views.attendance_report, name='attendance_report'),
    # 📝 Manual Attendance (backup)
    path('mark/<int:registration_id>/', views.mark_attendance, name='mark_attendance'),
]