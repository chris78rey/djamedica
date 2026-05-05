ROLE_ADMIN = "ADMIN"
ROLE_STAFF = "STAFF"


class BaseRoleAdminMixin:
    allowed_roles = ()

    def _is_allowed(self, request):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return getattr(user, "role", None) in self.allowed_roles

    def has_module_permission(self, request):
        return self._is_allowed(request)

    def has_view_permission(self, request, obj=None):
        return self._is_allowed(request)

    def has_add_permission(self, request):
        return self._is_allowed(request)

    def has_change_permission(self, request, obj=None):
        return self._is_allowed(request)

    def has_delete_permission(self, request, obj=None):
        return self._is_allowed(request)


class AdminOnlyAdminMixin(BaseRoleAdminMixin):
    allowed_roles = (ROLE_ADMIN,)


class StaffOrAdminAdminMixin(BaseRoleAdminMixin):
    allowed_roles = (ROLE_ADMIN, ROLE_STAFF)
