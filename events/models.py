from django.db import models
from django.conf import settings
from clubs.models import Club


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Write event details with line breaks")
    event_date = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title