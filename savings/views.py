from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment, Cashout
from .serializers import PaymentSerializer, CashoutSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CashoutViewSet(viewsets.ModelViewSet):

    serializer_class = CashoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cashout.objects.filter(user=self.request.user)