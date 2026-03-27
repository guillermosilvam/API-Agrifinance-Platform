# apps/accounts/permissions.py
from rest_framework import permissions

class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        user = request.user
        
        if is_authenticated and user.is_company:
            return hasattr(user, 'company_profile') and user.company_profile.status == 'verified'
        return False
    
class IsProducerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        has_profile = getattr(request.user, 'producer_profile', None) is not None
        
        return is_authenticated and request.user.is_producer and has_profile