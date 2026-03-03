from django.contrib import admin
from .models import Payment, Cashout, TransactionLedger


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "month", "status")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # If payment is approved, create ledger entry
        if obj.status == "Approved":

            exists = TransactionLedger.objects.filter(
                reference=f"PAY-{obj.id}"
            ).exists()

            if not exists:
                TransactionLedger.objects.create(
                    user=obj.user,
                    transaction_type="Payment",
                    amount=obj.amount,
                    reference=f"PAY-{obj.id}",
                    description="Savings payment approved"
                )


@admin.register(Cashout)
class CashoutAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_amount", "net_amount", "status")
    list_filter = ("status",)
    
@admin.register(TransactionLedger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_type", "amount", "reference", "created_at")