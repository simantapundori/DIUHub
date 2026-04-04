from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Club, Membership
from events.models import Event


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
        'clubs': clubs
    })


# ============================================
# Join a club
# ============================================
@login_required
def join_club(request, club_id):

    club = get_object_or_404(Club, id=club_id)

    Membership.objects.get_or_create(
        user=request.user,
        club=club,
        defaults={'status': 'pending'}
    )

    return redirect('club_list')


# ============================================
# Club Detail (🔥 NEW FEATURE)
# ============================================
@login_required
def club_detail(request, club_id):

    club = get_object_or_404(Club, id=club_id)

    # Check if user is approved member
    membership = Membership.objects.filter(
        user=request.user,
        club=club,
        status='approved'
    ).first()

    if not membership:
        return redirect('club_list')  # block access if not approved

    # Get events of this club
    events = Event.objects.filter(club=club).order_by('event_date')

    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'events': events
    })


# ============================================
# Membership Requests
# ============================================
@login_required
def membership_requests(request):

    clubs = Club.objects.filter(created_by=request.user)

    requests = Membership.objects.filter(
        club__in=clubs,
        status='pending'
    )

    return render(request, 'clubs/membership_requests.html', {
        'requests': requests
    })


# ============================================
# Approve membership
# ============================================
@login_required
def approve_membership(request, membership_id):

    membership = get_object_or_404(Membership, id=membership_id)
    membership.status = 'approved'
    membership.save()

    return redirect('membership_requests')


# ============================================
# Reject membership
# ============================================
@login_required
def reject_membership(request, membership_id):

    membership = get_object_or_404(Membership, id=membership_id)
    membership.status = 'rejected'
    membership.save()

    return redirect('membership_requests')