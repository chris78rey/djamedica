from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from apps.core.observability import audit_event


ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"
ROLE_DOCTOR = "DOCTOR"


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = ()
    raise_exception = True

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return getattr(user, "role", None) in self.allowed_roles

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No autorizado para esta operación.")
        return super().handle_no_permission()


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = (ROLE_ADMIN,)


class StaffOrAdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = (ROLE_ADMIN, ROLE_STAFF)


class ClinicalAccessRequiredMixin(RoleRequiredMixin):
    allowed_roles = (ROLE_ADMIN, ROLE_STAFF, ROLE_DOCTOR)


class AuditCreateMixin:
    audit_message = "Registro creado."

    def form_valid(self, form):
        response = super().form_valid(form)

        audit_event(
            request=self.request,
            action="CREATE",
            model_instance=self.object,
            message=self.audit_message,
            status_code=getattr(response, "status_code", None),
        )

        return response


class AuditUpdateMixin:
    audit_message = "Registro actualizado."

    def form_valid(self, form):
        response = super().form_valid(form)

        audit_event(
            request=self.request,
            action="UPDATE",
            model_instance=self.object,
            message=self.audit_message,
            status_code=getattr(response, "status_code", None),
        )

        return response


class DeleteSuccessMessageMixin:
    success_message = ""

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        object_pk = str(obj.pk)

        response = super().delete(request, *args, **kwargs)

        audit_event(
            request=request,
            action="DELETE",
            app_label=app_label,
            model_name=model_name,
            object_pk=object_pk,
            message=f"Registro eliminado: {obj}",
            status_code=getattr(response, "status_code", None),
        )

        if self.success_message:
            messages.success(request, self.success_message)

        return response
