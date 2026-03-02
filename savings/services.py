from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from .models import Payment


def get_total_approved_savings(user):
    total = Payment.objects.filter(
        user=user,
        status="Approved"
    ).aggregate(total=Sum("amount"))["total"]

    return total or Decimal("0.00")


def is_november_payment_approved(user):
    return Payment.objects.filter(
        user=user,
        month=11,
        status="Approved"
    ).exists()


def calculate_cashout_fee(user, requested_amount):
    """
    If November payment approved → 10%
    If NOT approved → 20%
    """
    if is_november_payment_approved(user):
        fee_percentage = 10
    else:
        fee_percentage = 20

    fee_amount = (Decimal(requested_amount) * Decimal(fee_percentage)) / Decimal(100)
    net_amount = Decimal(requested_amount) - fee_amount

    return fee_percentage, fee_amount, net_amount


@transaction.atomic
def process_cashout_request(user, requested_amount):
    total_savings = get_total_approved_savings(user)

    if Decimal(requested_amount) > total_savings:
        raise ValueError("Requested amount exceeds total savings.")

    fee_percentage, fee_amount, net_amount = calculate_cashout_fee(
        user,
        requested_amount
    )

    from .models import Cashout

    cashout = Cashout.objects.create(
        user=user,
        total_savings_snapshot=total_savings,
        requested_amount=requested_amount,
        fee_percentage=fee_percentage,
        fee_amount=fee_amount,
        net_amount=net_amount,
    )

    return cashout