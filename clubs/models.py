from django.db import models
from django.conf import settings

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    payment_ref = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user.username} -> {self.club.name}"
