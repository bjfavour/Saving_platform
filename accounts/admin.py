from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "username", "email", "telephone", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("telephone",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("telephone",)}),
    )

    search_fields = ("username", "email", "telephone")
    ordering = ("id",)