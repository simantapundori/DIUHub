from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    # users system (login, register, dashboard)
    path('', include('users.urls')),

    # clubs system
    path('clubs/', include('clubs.urls')),

]