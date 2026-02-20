from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('join/<int:club_id>/', views.join_club, name='join_club'),
]
