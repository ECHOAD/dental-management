from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    RoleChoices = (
        ("admin", "Administrator"),
        ("dentist", "Dentist"),
        ("assistant", "Assistant"),
    )

    role = models.CharField(max_length=20, choices=RoleChoices, default="dentist")

    def __str__(self):
        return f"{self.username} ({self.role})"
