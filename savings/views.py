from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment, Cashout, TransactionLedger
from .serializers import PaymentSerializer, CashoutSerializer
from .services import get_user_financial_summary


# ============================================================
# PAYMENT VIEWSET
# ============================================================

class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============================================================
# CASHOUT VIEWSET
# ============================================================

class CashoutViewSet(viewsets.ModelViewSet):

    serializer_class = CashoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cashout.objects.filter(user=self.request.user)


# ============================================================
# DASHBOARD SUMMARY VIEW
# ============================================================

class DashboardSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        summary = get_user_financial_summary(user)

        # Get latest 5 transactions
        transactions = TransactionLedger.objects.filter(
            user=user
        ).order_by("-created_at")[:5]

        recent_transactions = [
            {
                "date": t.created_at.strftime("%Y-%m-%d"),
                "type": t.transaction_type,
                "amount": str(t.amount),
                "reference": t.reference,
            }
            for t in transactions
        ]

        return Response({
            "total_payments": summary["total_payments"],
            "total_fees": summary["total_fees"],
            "total_cashouts": summary["total_cashouts"],
            "available_balance": summary["available_balance"],
            "recent_transactions": recent_transactions,
        })