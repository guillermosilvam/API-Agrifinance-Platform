# apps/accounts/permissions.py
from rest_framework import permissions

class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        has_profile = getattr(request.user, 'company_profile', None) is not None
        
        return is_authenticated and request.user.is_company and has_profile

class IsProducerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        has_profile = getattr(request.user, 'producer_profile', None) is not None
        
        return is_authenticated and request.user.is_producer and has_profile