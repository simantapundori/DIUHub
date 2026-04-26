from django.urls import path
from . import views

urlpatterns = [
    # 📊 Student Attendance
    path('', views.attendance_list, name='attendance_list'),

    # 📷 QR Scan
    path('scan/', views.scan_qr, name='scan_qr'),

    # 📊 Report
    path('report/', views.attendance_report, name='attendance_report'),

    # 👥 NEW
    path('event/<int:event_id>/students/', views.event_students, name='event_students'),

    # 📥 NEW
    path('event/<int:event_id>/export/', views.export_attendance, name='export_attendance'),

    # 📝 Manual
    path('mark/<int:registration_id>/', views.mark_attendance, name='mark_attendance'),
]