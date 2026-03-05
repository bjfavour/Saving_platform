from django.http import JsonResponse
from subscriptions.models import Subscriptions
from django.utils import timezone


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # APIs allowed even if expired
        allowed_paths = [
            "/admin",
            "/api/auth/login",
            "/api/auth/refresh",
            "/api/accounts/register",
            "/api/subscription/activate",
        ]

        for path in allowed_paths:
            if request.path.startswith(path):
                return self.get_response(request)

        # get latest subscription
        subscription = Subscriptions.objects.order_by("-id").first()

        # check expiry
        if subscription and subscription.expiry_date < timezone.now().date():
            return JsonResponse(
                {"detail": "Subscription expired"},
                status=403
            )

        return self.get_response(request)