from django.contrib import admin
from .models import Payment, Cashout


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "month", "status")
    list_filter = ("status", "month")


@admin.register(Cashout)
class CashoutAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_amount", "net_amount", "status")
    list_filter = ("status",)