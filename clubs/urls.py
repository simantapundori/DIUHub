from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('join/<int:club_id>/', views.join_club, name='join_club'),
    path('requests/', views.membership_requests, name='membership_requests'),
    path('requests/<int:membership_id>/approve/', views.approve_membership, name='approve_membership'),
    path('requests/<int:membership_id>/reject/', views.reject_membership, name='reject_membership'),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
] #new