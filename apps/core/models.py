from django.conf import settings
from django.db import models


class AuditEvent(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Creación"
        UPDATE = "UPDATE", "Actualización"
        DELETE = "DELETE", "Eliminación"
        LOGIN = "LOGIN", "Inicio de sesión"
        LOGOUT = "LOGOUT", "Cierre de sesión"
        ACCESS_DENIED = "ACCESS_DENIED", "Acceso denegado"
        VALIDATION = "VALIDATION", "Validación"
        ERROR = "ERROR", "Error"

    class Level(models.TextChoices):
        INFO = "INFO", "Información"
        WARNING = "WARNING", "Advertencia"
        ERROR = "ERROR", "Error"

    created_at = models.DateTimeField(auto_now_add=True)

    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.INFO,
    )

    action = models.CharField(
        max_length=30,
        choices=Action.choices,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
    )

    username = models.CharField(max_length=150, blank=True)

    app_label_field = models.CharField(max_length=80, blank=True)
    model_name = models.CharField(max_length=80, blank=True)
    object_pk = models.CharField(max_length=80, blank=True)

    path = models.CharField(max_length=500, blank=True)
    method = models.CharField(max_length=10, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    message = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["action"]),
            models.Index(fields=["level"]),
            models.Index(fields=["user"]),
            models.Index(fields=["app_label_field", "model_name"]),
        ]
        verbose_name = "Evento de auditoría"
        verbose_name_plural = "Eventos de auditoría"

    def __str__(self):
        return f"{self.created_at} | {self.action} | {self.username or 'anónimo'}"
