> **`registrations/views.py`**
import qrcode
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Registration
from events.models import Event
import os


@login_required
def register_event(request, event_id):

    event = Event.objects.get(id=event_id)

    registration, created = Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    if created:

        qr_data = f"user:{request.user.id},event:{event.id}"

        qr = qrcode.make(qr_data)

        filename = f"qr_user{request.user.id}_event{event.id}.png"

        filepath = os.path.join(settings.MEDIA_ROOT, 'qr_codes', filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        qr.save(filepath)

        registration.qr_code = f"qr_codes/{filename}"

        registration.save()

    return redirect('event_list')