from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'event',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'event',
        'created_at',
    )

    search_fields = (
        'user__username',
        'event__title',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
