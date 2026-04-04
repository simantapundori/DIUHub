from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Event
from registrations.models import Registration   


# ==========================================
# Show all events
# ==========================================
@login_required
def event_list(request):

    events = Event.objects.all().order_by('-event_date')  

    registrations = Registration.objects.filter(user=request.user)
    registered_events = [r.event.id for r in registrations]

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

    Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    return redirect('event_list')
    