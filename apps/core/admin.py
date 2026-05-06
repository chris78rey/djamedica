from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "level",
        "action",
        "username",
        "app_label_field",
        "model_name",
        "object_pk",
        "path",
        "status_code",
        "ip_address",
    )
    list_filter = (
        "level",
        "action",
        "app_label_field",
        "model_name",
        "created_at",
    )
    search_fields = (
        "username",
        "message",
        "path",
        "object_pk",
        "ip_address",
    )
    readonly_fields = (
        "created_at",
        "level",
        "action",
        "user",
        "username",
        "app_label_field",
        "model_name",
        "object_pk",
        "path",
        "method",
        "status_code",
        "ip_address",
        "user_agent",
        "message",
        "metadata",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
