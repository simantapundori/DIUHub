from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib import messages
import qrcode
from io import BytesIO

from .models import Event
from registrations.models import Registration
from clubs.models import Membership


# ==========================================
# Show all events
# ==========================================
@login_required
def event_list(request):

    events = Event.objects.all().order_by('-event_date')

    registered_events = Registration.objects.filter(
        user=request.user
    ).values_list('event_id', flat=True)

    # ✅ Get approved memberships
    user_memberships = Membership.objects.filter(
        user=request.user,
        status='approved'
    )

    user_clubs = [m.club.id for m in user_memberships]

    return render(request, 'events/event_list.html', {
        'events': events,
        'registered_events': registered_events,
        'user_clubs': user_clubs
    })


# ==========================================
# Register for event (WITH MEMBERSHIP CHECK)
# ==========================================
@login_required
def register_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    # 🔒 Check membership
    membership = Membership.objects.filter(
        user=request.user,
        club=event.club,
        status='approved'
    ).first()

    if not membership:
        messages.error(request, "❌ You must join this club to register for this event.")
        return redirect('event_list')

    registration, created = Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    # Generate QR only if new registration
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
# MY QR (STUDENT VIEW)
# ==========================================
@login_required
def my_qr(request):

    registrations = Registration.objects.filter(user=request.user)

    return render(request, 'events/my_qr.html', {
        'registrations': registrations
    })