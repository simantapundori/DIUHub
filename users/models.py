from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Club Admin'),
        ('advisor', 'Faculty Advisor'),
        ('committee', 'Committee Member'),
        ('superadmin', 'Super Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    full_name = models.CharField(max_length=100, blank=True)
    student_id = models.CharField(max_length=20, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    department = models.CharField(max_length=100, blank=True)
    batch = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username