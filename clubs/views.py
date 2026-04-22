from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Club, Membership
from events.models import Event
from registrations.models import Registration


# ============================================
# Show all clubs with membership status
# ============================================
@login_required
def club_list(request):

    clubs = Club.objects.all()

    memberships = Membership.objects.filter(user=request.user)

    membership_status = {}

    for membership in memberships:
        membership_status[membership.club.id] = membership.status

    for club in clubs:
        club.user_status = membership_status.get(club.id, None)

    return render(request, 'clubs/club_list.html', {
        'clubs': clubs,
    })


# ============================================
# Join a club
# ============================================
@login_required
@require_POST
def join_club(request, club_id):

    club = get_object_or_404(Club, id=club_id)

    Membership.objects.get_or_create(
        user=request.user,
        club=club,
        defaults={'status': 'pending', 'payment_ref': 'pending'}
    )

    return redirect('club_list')


# ============================================
# View membership requests (for club admin)
# ============================================
@login_required
def membership_requests(request):

    clubs = Club.objects.filter(created_by=request.user)

    requests = Membership.objects.filter(
        club__in=clubs,
        status='pending'
    )

    return render(request, 'clubs/membership_requests.html', {
        'requests': requests,
    })


# ============================================
# Approve membership
# ============================================
@login_required
@require_POST
def approve_membership(request, membership_id):

    membership = get_object_or_404(
        Membership,
        id=membership_id,
        club__created_by=request.user
    )

    membership.status = 'approved'
    membership.save()

    return redirect('membership_requests')


# ============================================
# Reject membership + DELETE registrations 🔥
# ============================================
@login_required
@require_POST
def reject_membership(request, membership_id):

    membership = get_object_or_404(
        Membership,
        id=membership_id,
        club__created_by=request.user
    )

    # 🔥 Remove all registrations of that club
    Registration.objects.filter(
        user=membership.user,
        event__club=membership.club
    ).delete()

    membership.status = 'rejected'
    membership.save()

    return redirect('membership_requests')


# ============================================
# Club Details and Event Inside (FIXED CLEAN)
# ============================================
@login_required
def club_detail(request, club_id):

    club = get_object_or_404(Club, id=club_id)

    events = Event.objects.filter(club=club).order_by('event_date')

    # Membership
    membership = Membership.objects.filter(
        user=request.user,
        club=club
    ).first()

    membership_status = membership.status if membership else None

    #  CLEAN FIX 
    registered_event_ids = list(
        Registration.objects.filter(user=request.user)
        .values_list('event_id', flat=True)
    )

    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'events': events,
        'membership_status': membership_status,
        'registered_event_ids': registered_event_ids
    })