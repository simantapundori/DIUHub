from django.db import models
from registrations.models import Registration

class Attendance(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attendance {self.registration.id}"
