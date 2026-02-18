from django.shortcuts import render, redirect
from django.utils import timezone
from registrations.models import Registration
from .models import Attendance


def mark_attendance(request, registration_id):

    registration = Registration.objects.get(id=registration_id)

    attendance, created = Attendance.objects.get_or_create(
        registration=registration
    )

    attendance.attended = True
    attendance.attended_at = timezone.now()

    attendance.save()

    return redirect('attendance_list')


def attendance_list(request):

    attendance = Attendance.objects.all()

    return render(request, 'attendance/attendance_list.html', {
        'attendance': attendance
    })