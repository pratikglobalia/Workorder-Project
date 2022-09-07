from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager') or request.user.groups.filter(name='employee')