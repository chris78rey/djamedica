from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.core.admin_mixins import AdminOnlyAdminMixin
from .models import User


@admin.register(User)
class UserAdmin(AdminOnlyAdminMixin, BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("role", "phone")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Información adicional", {"fields": ("email", "role", "phone")}),
    )
