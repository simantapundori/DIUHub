from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Club, Membership


# ============================================
# Show all clubs with membership status
# ============================================
@login_required
def club_list(request):

    # Get all clubs
    clubs = Club.objects.all()

    # Get current user's memberships
    memberships = Membership.objects.filter(user=request.user)

    # Create dictionary: club_id -> status
    membership_status = {}

    for membership in memberships:
        membership_status[membership.club.id] = membership.status

    # Attach status directly to each club object
    for club in clubs:
        club.user_status = membership_status.get(club.id, None)

    context = {
        'clubs': clubs,
    }

    return render(request, 'clubs/club_list.html', context)


# ============================================
# Join a club
# ============================================
@login_required
def join_club(request, club_id):

    club = get_object_or_404(Club, id=club_id)

    # Create membership only if it doesn't exist
    Membership.objects.get_or_create(
        user=request.user,
        club=club,
        defaults={'status': 'pending'}
    )

    return redirect('club_list')


# ============================================
# View membership requests (for club admin)
# ============================================
@login_required
def membership_requests(request):

    # Only clubs created by current user
    clubs = Club.objects.filter(created_by=request.user)

    # Get pending requests
    requests = Membership.objects.filter(
        club__in=clubs,
        status='pending'
    )

    context = {
        'requests': requests,
    }

    return render(request, 'clubs/membership_requests.html', context)


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