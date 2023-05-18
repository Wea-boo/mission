from rest_framework.permissions import BasePermission
from .models import Event

class IsAssigned(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assignee == request.user

class IsInvolved(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Event.objects.filter(demand=obj, trigger_user=request.user).exists()

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.main_profile.name == 'Missionaire' or request.user.groups.filter(group__profile__name='Missionaire').exists()

class IsSecretary(BasePermission): 
    def has_permission(self, request, view):
        return request.user.main_profile.name == 'Secrétaire' or request.user.groups.filter(group__profile__name='Secrétaire').exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.main_profile.name == 'Responsable Hierarchique' or request.user.groups.filter(group__profile__name='Responsable Hierarchique').exists()

class IsHRAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.main_profile.name == 'Agent RH' or request.user.groups.filter(group__profile__name='Agent RH').exists()

class IsHRManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.main_profile.name == 'Responsable RH' or request.user.groups.filter(group__profile__name='Responsable RH').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.main_profile.name == 'Administrateur' or request.user.groups.filter(group__profile__name='Administrateur').exists()

class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
