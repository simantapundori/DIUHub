from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Club, Membership


@login_required
def club_list(request):

    clubs = Club.objects.all()

    memberships = Membership.objects.filter(user=request.user)

    membership_dict = {}
    for membership in memberships:
        membership_dict[membership.club.id] = membership.status

    context = {
        'clubs': clubs,
        'membership_dict': membership_dict,
    }

    return render(request, 'clubs/club_list.html', context)


@login_required
def join_club(request, club_id):

    club = Club.objects.get(id=club_id)

    Membership.objects.get_or_create(
        user=request.user,
        club=club,
        defaults={'status': 'pending'}
    )

    return redirect('club_list')
