from django.contrib import admin

from apps.core.admin_mixins import StaffOrAdminAdminMixin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(StaffOrAdminAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "specialty",
        "scheduled_at",
        "duration_minutes",
        "status",
        "created_by",
    )
    list_filter = ("status", "specialty", "doctor")
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "patient__document_number",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "doctor__professional_license",
        "reason",
        "notes",
    )
    autocomplete_fields = ("patient", "doctor", "specialty", "created_by")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-scheduled_at",)
