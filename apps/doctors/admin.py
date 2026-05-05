from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
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
