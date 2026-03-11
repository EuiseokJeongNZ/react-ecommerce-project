from django.db import models
from .user import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    recipient = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    addr1 = models.CharField(max_length=255)
    addr2 = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.recipient}"