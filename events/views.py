from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib import messages
import qrcode
from io import BytesIO

from .models import Event
from registrations.models import Registration
from clubs.models import Membership, Club


# ==========================================
# 📅 EVENT LIST
# ==========================================
@login_required
def event_list(request):

    if request.user.role == "admin":
        events = Event.objects.filter(club=request.user.club).order_by('-event_date')
    else:
        events = Event.objects.all().order_by('-event_date')

    registered_events = Registration.objects.filter(
        user=request.user
    ).values_list('event_id', flat=True)

    user_memberships = Membership.objects.filter(
        user=request.user,
        status='approved'
    )
    user_clubs = [m.club.id for m in user_memberships]

    user_registrations = Registration.objects.filter(
        user=request.user
    ).select_related('event')

    registration_map = {
        r.event_id: r for r in user_registrations
    }

    for event in events:
        event.user_registration = registration_map.get(event.id)

    return render(request, 'events/event_list.html', {
        'events': events,
        'registered_events': registered_events,
        'user_clubs': user_clubs,
    })


# ==========================================
# ➕ CREATE EVENT
# ==========================================
@login_required
def create_event(request):

    if request.user.role not in ["admin", "superadmin"]:
        return redirect('dashboard')

    if request.user.role == "admin" and not request.user.club_id:
        messages.error(request, "❌ Your admin account is not assigned to a club.")
        return redirect('dashboard')

    clubs = None
    if request.user.role == "superadmin":
        clubs = Club.objects.all().order_by('name')

    if request.method == "POST":
        if request.user.role == "admin":
            club = request.user.club
        else:
            club_id = request.POST.get('club_id')
            if not club_id:
                messages.error(request, "❌ Please select a club.")
                return render(request, 'events/create_event.html', {'clubs': clubs})
            club = get_object_or_404(Club, id=club_id)

        Event.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            event_date=request.POST['event_date'],
            club=club,
            created_by=request.user
        )

        messages.success(request, "✅ Event created successfully!")
        return redirect('event_list')

    return render(request, 'events/create_event.html', {'clubs': clubs})


# ==========================================
# 📝 REGISTER EVENT
# ==========================================
@login_required
def register_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    membership = Membership.objects.filter(
        user=request.user,
        club=event.club,
        status='approved'
    ).first()

    if not membership:
        messages.error(request, "❌ You must join this club to register.")
        return redirect('event_list')

    registration, created = Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    if created:
        qr_data = f"{request.user.id}-{event.id}"

        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, format='PNG')

        file_name = f"user_{request.user.id}_event_{event.id}.png"

        registration.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=True)

        messages.success(request, "✅ Registered successfully!")

    else:
        messages.info(request, "ℹ️ Already registered.")

    return redirect('event_list')


# ==========================================
# 📱 MY QR
# ==========================================
@login_required
def my_qr(request):

    registrations = Registration.objects.filter(user=request.user)

    return render(request, 'events/my_qr.html', {
        'registrations': registrations
    })
