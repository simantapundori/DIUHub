
from django.db import models
from django.conf import settings
from clubs.models import Club


class Event(models.Model):
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='events'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    event_date = models.DateTimeField()   # renamed from "date"

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title