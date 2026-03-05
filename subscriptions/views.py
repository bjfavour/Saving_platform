from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import activate_subscription


class ActivateSubscriptionView(APIView):

    permission_classes = []  # Allow even if expired

    def post(self, request):

        license_key = request.data.get("license_key")

        if not license_key:
            return Response(
                {"detail": "PIN code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = activate_subscription(license_key)
            return Response(result)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )