from django.http import JsonResponse
from .models import Subscriptions


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow admin panel without subscription restriction
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        subscription = Subscriptions.objects.first()

        # If no subscription exists
        if not subscription:
            return JsonResponse(
                {"detail": "Subscription not configured."},
                status=403
            )

        # If subscription expired
        if not subscription.check_active():
            return JsonResponse(
                {"detail": "Subscription expired."},
                status=403
            )

        return self.get_response(request)