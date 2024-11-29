from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.save()
