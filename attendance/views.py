from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from openpyxl import Workbook

User = get_user_model()

from registrations.models import Registration
from events.models import Event
from .models import Attendance


# ==========================================
# 📷 QR SCAN (ADMIN ONLY + CLUB RESTRICT)
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

            registration = Registration.objects.select_related('user', 'event').get(
                user_id=user_id,
                event_id=event_id
            )

            # 🔐 CLUB SECURITY
            if request.user.role == "admin" and registration.event.club != request.user.club:
                return JsonResponse({"error": "Unauthorized"}, status=403)

            attendance, created = Attendance.objects.get_or_create(
                registration=registration
            )

            if attendance.attended:
                return JsonResponse({
                    "status": "already",
                    "message": "⚠️ Already marked",
                    "student_name": registration.user.username,
                    "student_id": getattr(registration.user, 'student_id', registration.user.id),
                    "event": registration.event.title
                })

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

    return render(request, 'attendance/scan.html')

# ==========================================
# 📊 STUDENT ATTENDANCE LIST (FINAL)
# ==========================================
@login_required
def attendance_list(request):

    # 🔐 Admin → only see own club attendance
    if request.user.role == "admin":
        attendance = Attendance.objects.filter(
            registration__event__club=request.user.club
        ).select_related(
            'registration__event',
            'registration__user',
            'registration__event__club'
        )

    # 👤 Student → only own attendance
    else:
        attendance = Attendance.objects.filter(
            registration__user=request.user
        ).select_related(
            'registration__event',
            'registration__user',
            'registration__event__club'
        )

    return render(request, 'attendance/attendance_list.html', {
        'attendance': attendance
    })
# ==========================================
# 📊 ADMIN ATTENDANCE REPORT (CLUB FILTERED)
# ==========================================
@login_required
def attendance_report(request):

    if request.user.role not in ["admin", "superadmin"]:
        return redirect('dashboard')

    # 🔐 FILTER EVENTS
    if request.user.role == "admin":
        events = Event.objects.filter(club=request.user.club)
    else:
        events = Event.objects.all()

    events = events.order_by('-event_date')

    report = []

    for event in events:

        total = Registration.objects.filter(event=event).count()

        present = Attendance.objects.filter(
            registration__event=event,
            attended=True
        ).count()

        report.append({
            'event': event,
            'club': event.club,
            'total_registered': total,
            'present': present,
            'absent': total - present
        })

    return render(request, 'attendance/attendance_report.html', {
        'report': report
    })


# ==========================================
# 👥 VIEW STUDENTS (NEW 🔥)
# ==========================================
@login_required
def event_students(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if request.user.role == "admin" and event.club != request.user.club:
        return redirect('dashboard')

    registrations = Registration.objects.filter(event=event).select_related('user')

    students = []

    for reg in registrations:

        attendance = Attendance.objects.filter(
            registration=reg,
            attended=True
        ).first()

        students.append({
            'name': reg.user.username,
            'student_id': getattr(reg.user, 'student_id', reg.user.id),
            'status': 'Present' if attendance else 'Absent'
        })

    return render(request, 'attendance/event_students.html', {
        'students': students,
        'event': event
    })


# ==========================================
# 📥 EXPORT EXCEL (NEW 🔥)
# ==========================================
@login_required
def export_attendance(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if request.user.role == "admin" and event.club != request.user.club:
        return HttpResponse("Unauthorized", status=403)

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    ws.append(["Name", "Student ID", "Status"])

    registrations = Registration.objects.filter(event=event).select_related('user')

    for reg in registrations:

        attendance = Attendance.objects.filter(
            registration=reg,
            attended=True
        ).first()

        status = "Present" if attendance else "Absent"

        ws.append([
            reg.user.username,
            getattr(reg.user, 'student_id', reg.user.id),
            status
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="attendance.xlsx"'

    wb.save(response)
    return response

@login_required
def attendance_list(request):

    if request.user.role == "admin":
        attendance = Attendance.objects.filter(
            registration__event__club=request.user.club
        ).select_related(
            'registration__event',
            'registration__user',
            'registration__event__club'
        )
    else:
        attendance = Attendance.objects.filter(
            registration__user=request.user
        ).select_related(
            'registration__event',
            'registration__user',
            'registration__event__club'
        )

    return render(request, 'attendance/attendance_list.html', {
        'attendance': attendance
    })
@login_required
def mark_attendance(request, registration_id):

    registration = get_object_or_404(Registration, id=registration_id)

    # 🔐 Restrict admin to own club
    if request.user.role == "admin" and registration.event.club != request.user.club:
        return redirect('dashboard')

    attendance, created = Attendance.objects.get_or_create(
        registration=registration
    )

    attendance.attended = True
    attendance.attended_at = timezone.now()
    attendance.save()

    return redirect('attendance_list')