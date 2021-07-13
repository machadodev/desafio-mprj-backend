from rest_framework.permissions import BasePermission

class PermissionDocumento(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('desafio.view_document')
