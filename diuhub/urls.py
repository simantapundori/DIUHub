from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    # users system
    path('', include('users.urls')),

    # clubs system
    path('clubs/', include('clubs.urls')),

    # events system
    path('events/', include('events.urls')),

    # attendance system
    path('attendance/', include('attendance.urls')),

]