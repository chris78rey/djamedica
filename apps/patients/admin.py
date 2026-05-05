from django.contrib import admin

from apps.core.admin_mixins import StaffOrAdminAdminMixin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(StaffOrAdminAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "document_type",
        "document_number",
        "first_name",
        "last_name",
        "phone",
        "email",
        "is_active",
    )
    list_filter = ("document_type", "is_active", "sex")
    search_fields = (
        "document_number",
        "first_name",
        "last_name",
        "phone",
        "email",
    )
    ordering = ("last_name", "first_name")
