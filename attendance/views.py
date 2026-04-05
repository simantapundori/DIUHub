from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from registrations.models import Registration
from .models import Attendance


# ==========================================
# QR SCAN ATTENDANCE (MAIN FEATURE)
# ==========================================
@login_required
def scan_qr(request):

    message = ""

    if request.method == "POST":
        qr_data = request.POST.get('qr_data')

        try:
            user_id, event_id = qr_data.split('-')

            registration = Registration.objects.get(
                user_id=user_id,
                event_id=event_id
            )

            Attendance.objects.get_or_create(
                registration=registration
            )

            message = "✅ Attendance marked successfully"

        except:
            message = "❌ Invalid QR Code"

    return render(request, 'attendance/scan.html', {
        'message': message
    })


# ==========================================
# ATTENDANCE LIST
# ==========================================
@login_required
def attendance_list(request):

    attendance = Attendance.objects.all()

    return render(request, 'attendance/attendance_list.html', {
        'attendance': attendance
    })


# ==========================================
# MANUAL MARK (KEEP FOR BACKUP)
# ==========================================
@login_required
def mark_attendance(request, registration_id):

    registration = get_object_or_404(Registration, id=registration_id)

    attendance, created = Attendance.objects.get_or_create(
        registration=registration
    )

    attendance.attended = True
    attendance.save()

    return redirect('attendance_list')