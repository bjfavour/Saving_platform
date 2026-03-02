from django.contrib import admin
from .models import Subscriptions


@admin.register(Subscriptions)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("license_type", "start_date", "expiry_date", "is_active")