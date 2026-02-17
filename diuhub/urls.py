from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # connect users app URLs
    path('', include('users.urls')),
]
