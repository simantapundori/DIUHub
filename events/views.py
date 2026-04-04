from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from .models import Event
from registrations.models import Registration


# ==========================================
# Show all events
# ==========================================
@login_required
def event_list(request):

    events = Event.objects.all().order_by('-event_date')

    registered_events = Registration.objects.filter(
        user=request.user
    ).values_list('event_id', flat=True)

    return render(request, 'events/event_list.html', {
        'events': events,
        'registered_events': registered_events
    })


# ==========================================
# Register for event
# ==========================================
@login_required
def register_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

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

    return redirect('event_list')