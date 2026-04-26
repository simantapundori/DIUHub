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

    # Blood Group choices
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # Department choices
    DEPARTMENT_CHOICES = [
        ('CSE', 'CSE'),
        ('SWE', 'Software Engineering'),
        ('EEE', 'EEE'),
        ('BBA', 'BBA'),
        ('ENG', 'English'),
    ]

    # ===============================
    # ROLE
    # ===============================
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    # ===============================
    # 🔥 NEW: CLUB ASSIGNMENT
    # ===============================
    club = models.ForeignKey(
    'clubs.Club',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='club_admins'
)


    # ===============================
    # PROFILE FIELDS
    # ===============================
    full_name = models.CharField(max_length=100, blank=True)
    student_id = models.CharField(max_length=20, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
        blank=True
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        blank=True
    )

    batch = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=10, blank=True)

    # ===============================
    # AUTO ROLE LOGIC 
    # ===============================
    def save(self, *args, **kwargs):

        if self.is_superuser:
            self.role = "superadmin"

        elif not self.role:
            self.role = "student"

        super().save(*args, **kwargs)