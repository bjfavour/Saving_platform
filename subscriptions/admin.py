from django.contrib import admin
from .models import Subscriptions
from .models import LicenseKey

@admin.register(LicenseKey)
class LicenseKeyAdmin(admin.ModelAdmin):
    list_display = ("pin_code", "plan_type", "is_used", "created_at")


@admin.register(Subscriptions)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("license_type", "start_date", "expiry_date", "is_active")