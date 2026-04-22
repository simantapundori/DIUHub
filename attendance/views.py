from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

from registrations.models import Registration
from events.models import Event
from .models import Attendance


# ==========================================
# 📷 QR SCAN (ADMIN + SUPERADMIN ONLY)
# ==========================================
@login_required
def scan_qr(request):

    # 🔒 Restrict access
    if request.user.role not in ["admin", "superadmin"]:
        if request.method == "GET":
            messages.error(request, "❌ Access denied")
            return redirect('dashboard')
        return JsonResponse({"error": "Access denied"}, status=403)

    # ✅ FIXED INDENTATION HERE
    if request.method == "POST":

        qr_data = request.POST.get('qr_data')

        try:
            user_id, event_id = qr_data.split('-')

            registration = Registration.objects.select_related(
                'user', 'event'
            ).get(
                user_id=user_id,
                event_id=event_id
            )

            attendance, created = Attendance.objects.get_or_create(
                registration=registration
            )

            # ⚠️ Already marked
            if attendance.attended:
                return JsonResponse({
                    "status": "already",
                    "message": "⚠️ Already marked",
                    "student_name": registration.user.username,
                    "student_id": getattr(registration.user, 'student_id', registration.user.id),
                    "event": registration.event.title
                })

            # ✅ Mark attendance
            attendance.attended = True
            attendance.attended_at = timezone.now()
            attendance.save()

            return JsonResponse({
                "status": "success",
                "message": "✅ Attendance marked",
                "student_name": registration.user.username,
                "student_id": getattr(registration.user, 'student_id', registration.user.id),
                "event": registration.event.title
            })

        except Exception:
            return JsonResponse({
                "status": "error",
                "message": "❌ Invalid QR"
            }, status=400)

    # 🔥 IMPORTANT (you missed this before)
    return render(request, 'attendance/scan.html')


# ==========================================
# 📊 STUDENT ATTENDANCE
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
# 📊 ADMIN ATTENDANCE REPORT
# ==========================================
@login_required
def attendance_report(request):

    if request.user.role not in ["admin", "superadmin"]:
        return redirect('dashboard')

    events = Event.objects.all().order_by('-event_date')

    report = []

    for event in events:

        total_registered = Registration.objects.filter(event=event).count()

        total_present = Attendance.objects.filter(
            registration__event=event,
            attended=True
        ).count()

        total_absent = total_registered - total_present

        report.append({
            'event': event,
            'club': event.club,
            'total_registered': total_registered,
            'present': total_present,
            'absent': total_absent
        })

    return render(request, 'attendance/attendance_report.html', {
        'report': report
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