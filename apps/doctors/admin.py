from django.contrib import admin

from apps.core.admin_mixins import AdminOnlyAdminMixin
from .models import Doctor, DoctorSpecialtyCredential


@admin.register(Doctor)
class DoctorAdmin(AdminOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "specialty",
        "professional_license",
        "phone",
        "office",
        "is_available",
    )
    list_filter = ("specialty", "is_available")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "professional_license",
        "phone",
    )
    autocomplete_fields = ("user", "specialty")
    ordering = ("user__last_name", "user__first_name")


@admin.register(DoctorSpecialtyCredential)
class DoctorSpecialtyCredentialAdmin(AdminOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "specialty",
        "status",
        "registration_code",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    )
    list_filter = ("status", "specialty")
    search_fields = (
        "doctor__user__username",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "doctor__professional_license",
        "specialty__name",
        "registration_code",
    )
    autocomplete_fields = ("doctor", "specialty", "reviewed_by")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("doctor__user__last_name", "doctor__user__first_name")
