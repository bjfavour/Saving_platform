from django.utils import timezone
from datetime import timedelta
from .models import LicenseKey, Subscriptions


def activate_subscription(pin_code):

    try:
        license_key = LicenseKey.objects.get(pin_code=pin_code, is_used=False)
    except LicenseKey.DoesNotExist:
        raise ValueError("Invalid or already used PIN.")

    subscription = Subscriptions.objects.first()

    if not subscription:
        raise ValueError("Subscription record not found.")

    today = timezone.now().date()

    if license_key.plan_type == "monthly":
        new_expiry = today + timedelta(days=30)

    elif license_key.plan_type == "quarterly":
        new_expiry = today + timedelta(days=90)

    elif license_key.plan_type == "yearly":
        new_expiry = today + timedelta(days=365)

    subscription.expiry_date = new_expiry
    subscription.is_active = True
    subscription.save()

    license_key.is_used = True
    license_key.used_at = timezone.now()
    license_key.save()

    return {
        "message": "Subscription activated successfully.",
        "new_expiry_date": new_expiry,
        "plan": license_key.plan_type,
    }