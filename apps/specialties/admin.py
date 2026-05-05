from django.contrib import admin

from apps.core.admin_mixins import AdminOnlyAdminMixin
from .models import Specialty


@admin.register(Specialty)
class SpecialtyAdmin(AdminOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("name",)
