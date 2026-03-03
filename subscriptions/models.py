from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class LicenseKey(models.Model):

    PLAN_CHOICES = (
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("yearly", "Yearly"),
    )

    pin_code = models.CharField(max_length=50, unique=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pin_code} - {self.plan_type}"


class Subscriptions(models.Model):

    LICENSE_TYPES = (
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Yearly", "Yearly"),
    )

    license_type = models.CharField(max_length=20, choices=LICENSE_TYPES)

    start_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        SINGLE-TENANT ENFORCEMENT:
        Only ONE subscription record is allowed.
        """

        # Prevent multiple subscription records
        if not self.pk and Subscriptions.objects.exists():
            raise ValidationError(
                "Only one subscription allowed for single-tenant system."
            )

        # Auto calculate expiry date if not provided
        if not self.expiry_date:
            if self.license_type == "Monthly":
                self.expiry_date = self.start_date + timedelta(days=30)
            elif self.license_type == "Quarterly":
                self.expiry_date = self.start_date + timedelta(days=90)
            elif self.license_type == "Yearly":
                self.expiry_date = self.start_date + timedelta(days=365)

        # Auto deactivate if expired
        if self.expiry_date and timezone.now().date() > self.expiry_date:
            self.is_active = False

        super().save(*args, **kwargs)

    def check_active(self):
        """
        Call this before processing protected APIs
        """
        if timezone.now().date() > self.expiry_date:
            self.is_active = False
            self.save(update_fields=["is_active"])
        return self.is_active

    def is_expired(self):
        return timezone.now().date() > self.expiry_date

    def __str__(self):
        return f"{self.license_type} - Expires {self.expiry_date}"