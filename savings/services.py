from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from .models import Payment, Cashout, TransactionLedger


# ============================================================
# BALANCE CALCULATIONS
# ============================================================

def get_user_available_balance(user):
    """
    Real available balance using ledger.
    Balance = Payments - Fees - Cashouts
    """

    payments = TransactionLedger.objects.filter(
        user=user,
        transaction_type="Payment"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    fees = TransactionLedger.objects.filter(
        user=user,
        transaction_type="Fee"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    cashouts = TransactionLedger.objects.filter(
        user=user,
        transaction_type="Cashout"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    return payments - fees - cashouts


def get_user_financial_summary(user):
    """
    Returns full financial breakdown.
    """

    payments = TransactionLedger.objects.filter(
        user=user,
        transaction_type="Payment"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    fees = TransactionLedger.objects.filter(
        user=user,
        transaction_type="Fee"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    cashouts = TransactionLedger.objects.filter(
        user=user,
        transaction_type="Cashout"
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    balance = payments - fees - cashouts
    preview_admin_fee = balance * Decimal("0.10")
    preview_net_cashout = balance - preview_admin_fee

    return {
        "total_payments": payments,
        "total_fees": fees,
        "total_cashouts": cashouts,
        "available_balance": balance,
        "admin_fee_preview": preview_admin_fee,
        "net_cashout_preview": preview_net_cashout,
    }


# ============================================================
# BUSINESS RULE CHECKS
# ============================================================

def is_november_payment_approved(user):
    return Payment.objects.filter(
        user=user,
        month=11,
        status="Approved"
    ).exists()


def has_paid_this_month(user):
    current_month = timezone.now().month

    return Payment.objects.filter(
        user=user,
        month=current_month,
        status="Approved"
    ).exists()


# ============================================================
# CASHOUT FEE LOGIC
# ============================================================

def calculate_cashout_fee(user, requested_amount):
    """
    Jan–Oct → 20%
    Nov–Dec → 10%
    """

    requested_amount = Decimal(requested_amount)

    current_month = timezone.now().month

    if current_month < 11:
        fee_percentage = Decimal("20")
    else:
        fee_percentage = Decimal("10")

    fee_amount = (requested_amount * fee_percentage) / Decimal("100")

    net_amount = requested_amount - fee_amount

    return fee_percentage, fee_amount, net_amount


# ============================================================
# CASHOUT PROCESSING
# ============================================================

@transaction.atomic
def process_cashout_request(user, requested_amount):
    """
    Ledger-based cashout engine.
    """

    requested_amount = Decimal(requested_amount)

    if not has_paid_this_month(user):
        raise ValueError("You must save at least once this month before cashout.")

    available_balance = get_user_available_balance(user)

    if requested_amount > available_balance:
        raise ValueError("Requested amount exceeds available balance.")

    fee_percentage, fee_amount, net_amount = calculate_cashout_fee(
        user, requested_amount
    )

    cashout = Cashout.objects.create(
        user=user,
        total_savings_snapshot=available_balance,
        requested_amount=requested_amount,
        fee_percentage=fee_percentage,
        fee_amount=fee_amount,
        net_amount=net_amount,
    )

    # Ledger entries
    TransactionLedger.objects.create(
        user=user,
        transaction_type="Cashout",
        amount=net_amount,
        reference=f"CASH-{cashout.id}",
        description="Cashout processed"
    )

    TransactionLedger.objects.create(
        user=user,
        transaction_type="Fee",
        amount=fee_amount,
        reference=f"FEE-{cashout.id}",
        description=f"{fee_percentage}% administrative fee"
    )

    return cashout


# ============================================================
# PDF STATEMENT GENERATOR (WITH FULL TRANSACTION HISTORY)
# ============================================================

def generate_user_statement_pdf(user):
    """
    Generates full PDF statement including transaction history.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    summary = get_user_financial_summary(user)

    # Title
    elements.append(Paragraph(f"<b>Financial Statement - {user.username}</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Summary Section
    elements.append(Paragraph("Summary:", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Total Payments: ₦ {summary['total_payments']}", styles["Normal"]))
    elements.append(Paragraph(f"Total Fees: ₦ {summary['total_fees']}", styles["Normal"]))
    elements.append(Paragraph(f"Total Cashouts: ₦ {summary['total_cashouts']}", styles["Normal"]))
    elements.append(Paragraph(f"Available Balance: ₦ {summary['available_balance']}", styles["Normal"]))
    elements.append(Paragraph(f"Net After 10% Preview: ₦ {summary['net_cashout_preview']}", styles["Normal"]))

    elements.append(Spacer(1, 0.5 * inch))

    # Transaction History Table
    elements.append(Paragraph("Transaction History:", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    transactions = TransactionLedger.objects.filter(user=user).order_by("-created_at")

    data = [["Date", "Type", "Amount", "Reference"]]

    for tx in transactions:
        data.append([
            tx.created_at.strftime("%Y-%m-%d"),
            tx.transaction_type,
            f"₦ {tx.amount}",
            tx.reference,
        ])

    table = Table(data, colWidths=[1.2*inch, 1*inch, 1*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return buffer