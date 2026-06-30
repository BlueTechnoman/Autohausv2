#Hier wird festgelegt wer auf welche API zugreifen darf (RH, NW)
from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ["employee", "admin"]
        )
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "customer"
        )