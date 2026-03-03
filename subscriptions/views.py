from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import activate_subscription


class ActivateSubscriptionView(APIView):

    permission_classes = []  # Allow even if expired

    def post(self, request):

        pin_code = request.data.get("pin_code")

        if not pin_code:
            return Response(
                {"detail": "PIN code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = activate_subscription(pin_code)
            return Response(result)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )