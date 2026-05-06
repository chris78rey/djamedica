import logging

from django.utils.text import Truncator

from apps.core.models import AuditEvent


audit_logger = logging.getLogger("djamedica.audit")
request_logger = logging.getLogger("djamedica.request")
error_logger = logging.getLogger("djamedica.error")


def get_client_ip(request):
    if not request:
        return None

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def get_user_agent(request):
    if not request:
        return ""

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    return Truncator(user_agent).chars(500)


def get_request_user(request):
    if not request:
        return None

    user = getattr(request, "user", None)

    if user and user.is_authenticated:
        return user

    return None


def audit_event(
    *,
    request=None,
    action,
    level=AuditEvent.Level.INFO,
    model_instance=None,
    app_label="",
    model_name="",
    object_pk="",
    message="",
    status_code=None,
    metadata=None,
):
    """
    Registra eventos importantes sin guardar datos sensibles.
    No debe usarse para guardar passwords, tokens, cookies ni contenido clínico completo.
    """

    try:
        user = get_request_user(request)

        if model_instance is not None:
            meta = model_instance._meta
            app_label = app_label or meta.app_label
            model_name = model_name or meta.model_name
            object_pk = object_pk or str(getattr(model_instance, "pk", "") or "")

        event = AuditEvent.objects.create(
            level=level,
            action=action,
            user=user,
            username=getattr(user, "username", "") if user else "",
            app_label_field=app_label,
            model_name=model_name,
            object_pk=str(object_pk or ""),
            path=getattr(request, "path", "") if request else "",
            method=getattr(request, "method", "") if request else "",
            status_code=status_code,
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
            message=Truncator(message or "").chars(500),
            metadata=metadata or {},
        )

        audit_logger.info(
            "audit_event id=%s action=%s user=%s model=%s.%s object_pk=%s path=%s",
            event.id,
            event.action,
            event.username or "anonymous",
            event.app_label_field,
            event.model_name,
            event.object_pk,
            event.path,
        )

        return event

    except Exception:
        error_logger.exception("No se pudo guardar AuditEvent.")
        return None
