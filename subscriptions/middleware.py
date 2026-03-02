from django.http import JsonResponse
from .models import Subscriptions


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow admin panel always
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # Only protect API routes
        if request.path.startswith("/api/"):

            subscription = Subscriptions.objects.first()

            if not Subscriptions:
                return JsonResponse(
                    {"detail": "Subscription Not Activated"},
                    status=403
                )

            if not Subscriptions.check_active():
                return JsonResponse(
                    {"detail": "Subscription Expired"},
                    status=403
                )

        return self.get_response(request)