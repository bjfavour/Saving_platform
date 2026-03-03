from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.http import HttpResponse
from django.middleware.csrf import get_token

from .models import User
from savings.services import (
    get_user_financial_summary,
    generate_user_statement_pdf,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "username",
        "email",
        "telephone",
        "is_active",
        "is_staff",
        "is_approved",
    )

    readonly_fields = ("financial_summary",)

    list_filter = ("is_active", "is_staff", "is_superuser", "is_approved")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "telephone",
                "role",
                "is_approved",
                "full_name",
                "address",
                "bank_name",
                "bank_account_number",
                "profile_picture",
            )
        }),
        ("Financial Report", {
            "fields": ("financial_summary",)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("telephone", "role")
        }),
    )

    search_fields = ("username", "email", "telephone")
    ordering = ("id",)

    # ============================================================
    # BEAUTIFUL FINANCIAL REPORT DISPLAY
    # ============================================================

    def financial_summary(self, obj):
        summary = get_user_financial_summary(obj)

        return format_html(
            """
            <div style="padding:20px; background:#f4f6f9; border-radius:12px;">
                <h3 style="color:#2c3e50;">💰 Financial Summary</h3>
                <hr>
                <p><strong>Total Payments:</strong> ₦ {}</p>
                <p style="color:#c0392b;"><strong>Total Fees:</strong> ₦ {}</p>
                <p><strong>Total Cashouts:</strong> ₦ {}</p>
                <p style="color:green; font-size:16px;">
                    <strong>Available Balance:</strong> ₦ {}
                </p>
                <p style="color:#2980b9;">
                    <strong>Net After 10% (Preview):</strong> ₦ {}
                </p>
                <br>
                <button type="submit" name="_download_pdf"
                    style="background:#2c3e50; color:white; padding:8px 15px; border:none; border-radius:6px;">
                    📄 Download PDF Statement
                </button>
            </div>
            """,
            summary["total_payments"],
            summary["total_fees"],
            summary["total_cashouts"],
            summary["available_balance"],
            summary["net_cashout_preview"],
        )

    financial_summary.short_description = "Financial Report"

    # ============================================================
    # HANDLE PDF DOWNLOAD BUTTON
    # ============================================================

    def response_change(self, request, obj):
        if "_download_pdf" in request.POST:
            pdf = generate_user_statement_pdf(obj)

            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="{obj.username}_statement.pdf"'
            )
            return response

        return super().response_change(request, obj)