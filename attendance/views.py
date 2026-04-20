from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta

from registrations.models import Registration
from .models import Attendance


# ==========================================
# 📷 QR SCAN (ADMIN + SUPERADMIN ONLY)
# ==========================================
@login_required
def scan_qr(request):

    if request.user.role not in ["admin", "superadmin"]:
        if request.method == "GET":
            messages.error(request, "❌ Access denied")
            return redirect('dashboard')
        return JsonResponse({"error": "Access denied"}, status=403)

    if request.method == "POST":

        qr_data = request.POST.get('qr_data')

        try:
            user_id, event_id = qr_data.split('-')

            registration = Registration.objects.get(
                user_id=user_id,
                event_id=event_id
            )

            attendance, created = Attendance.objects.get_or_create(
                registration=registration
            )

            # prevent duplicate
            if attendance.attended:
                return JsonResponse({
                    "status": "already",
                    "message": "⚠️ Already marked"
                })

            attendance.attended = True
            attendance.attended_at = timezone.now()
            attendance.save()

            return JsonResponse({
                "status": "success",
                "message": "✅ Attendance marked"
            })

        except Exception:
            return JsonResponse({
                "status": "error",
                "message": "❌ Invalid QR"
            }, status=400)

    return render(request, 'attendance/scan.html')


# ==========================================
# 📊 ATTENDANCE LIST
# ==========================================
@login_required
def attendance_list(request):

    attendance = Attendance.objects.filter(
        registration__user=request.user
    ).select_related(
        'registration__event',
        'registration__user'
    )

    return render(request, 'attendance/attendance_list.html', {
        'attendance': attendance
    })


# ==========================================
# 📝 MANUAL MARK (BACKUP)
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