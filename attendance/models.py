from django.db import models
from registrations.models import Registration


class Attendance(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    attended = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration.user.username} - {self.registration.event.title}"