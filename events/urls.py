from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),

    # 🔥 NEW
    path('create/', views.create_event, name='create_event'),

    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('my-qr/', views.my_qr, name='my_qr'),
]