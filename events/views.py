from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event


@login_required
def event_list(request):

    events = Event.objects.all().order_by('-event_date')

    return render(request, 'events/event_list.html', {
        'events': events
    })
    