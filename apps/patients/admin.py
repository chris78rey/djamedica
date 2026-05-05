from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
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
