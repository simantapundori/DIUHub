from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import json

from registrations.models import Registration
from .models import Attendance


# ==========================================
# QR CAMERA SCAN ATTENDANCE 
# ==========================================
@login_required
def scan_qr(request):

    # 🔒 Restrict to admin only
    if request.user.role not in ["admin", "superadmin"]:
        return redirect('dashboard')

    # ✅ Handle camera scan (AJAX / JSON)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            qr_data = data.get("qr_data")

            # Expecting format: user_id-event_id
            user_id, event_id = qr_data.split("-")

            registration = Registration.objects.get(
                user_id=user_id,
                event_id=event_id
            )

            attendance, created = Attendance.objects.get_or_create(
                registration=registration
            )

            attendance.attended = True
            attendance.attended_at = timezone.now()
            attendance.save()

            return JsonResponse({
                "message": "✅ Attendance marked successfully"
            })

        except Exception as e:
            return JsonResponse({
                "message": "❌ Invalid QR Code"
            })

    # ✅ Load scan page
    return render(request, 'attendance/scan.html')


# ==========================================
# ATTENDANCE LIST
# ==========================================
@login_required
def attendance_list(request):

    attendance = Attendance.objects.filter(
        registration__user=request.user
    )

    return render(request, 'attendance/attendance_list.html', {
        'attendance': attendance
    })


# ==========================================
# MANUAL MARK (BACKUP)
# ==========================================
@login_required
def mark_attendance(request, registration_id):

    registration = get_object_or_404(Registration, id=registration_id)

    attendance, created = Attendance.objects.get_or_create(
        registration=registration
    )

    attendance.attended = True
    attendance.attended_at = timezone.now()
    attendance.save()

    return redirect('attendance_list')