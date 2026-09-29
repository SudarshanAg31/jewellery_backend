from django.db import models
import secrets


class DeviceActivation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('ACTIVE', 'Active'),
        ('BLOCKED', 'Blocked'),
    ]

    device_id = models.CharField(max_length=128, unique=True, db_index=True)
    device_name = models.CharField(max_length=255, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    activation_token = models.CharField(max_length=128, blank=True, null=True)

    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    admin_note = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.device_name or 'Unknown'} - {self.status}"

    def generate_token(self):
        self.activation_token = secrets.token_urlsafe(48)
        return self.activation_token