from rest_framework.permissions import SAFE_METHODS, BasePermission
 
 
class IsAdmin(BasePermission):
    """Authenticated, active staff user. Everything else is a Visitor."""
 
    message = "Only admin can perform this action."
 
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
 
 
class IsAdminOrReadOnly(BasePermission):
    """Visitors: read only. Admin: full access."""
 
    message = "Only admin can create, update or delete."
 
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return IsAdmin().has_permission(request, view)
 
 
class AllowCreateOrAdmin(BasePermission):
    """Public forms (booking, contact, applications): visitors may POST only.
    Reading, updating and deleting submissions is admin only."""
 
    message = "Only admin can view or manage submissions."
 
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return IsAdmin().has_permission(request, view)
 