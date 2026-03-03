from django.utils import timezone
from django.http import JsonResponse
from .models import Subscriptions


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow admin always
        if request.path.startswith("/admin"):
            return self.get_response(request)

        # ✅ Allow activation endpoint even if expired
        if request.path.startswith("/api/subscription/activate"):
            return self.get_response(request)

        subscription = Subscriptions.objects.first()

        if not subscription:
            return JsonResponse(
                {"detail": "Subscription not configured."},
                status=403
            )

        if not subscription.is_active:
            return JsonResponse(
                {"detail": "Subscription expired."},
                status=403
            )

        if subscription.expiry_date < timezone.now().date():
            return JsonResponse(
                {"detail": "Subscription expired."},
                status=403
            )

        return self.get_response(request)