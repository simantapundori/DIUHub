from django.contrib import admin
from django.urls import path, include

# ✅ Required for media files (QR codes, uploads)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Users system
    path('', include('users.urls')),

    # Clubs system
    path('clubs/', include('clubs.urls')),

    # Events system
    path('events/', include('events.urls')),

    # Attendance system
    path('attendance/', include('attendance.urls')),
]


# ✅ Serve media files in development 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)