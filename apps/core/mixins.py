from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


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


class DeleteSuccessMessageMixin:
    success_message = ""

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(request, self.success_message)
        return response
