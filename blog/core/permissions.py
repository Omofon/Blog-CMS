from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import TYPE_CHECKING, Mapping

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

if TYPE_CHECKING:
    from rest_framework.permissions import _SupportsHasPermission


def get_user(request: Request) -> User:
    # get user for authentication

    user = request.user
    assert isinstance(user, User)
    return user

def has_group(user: User, group: str) -> bool:
    return user.groups.filter(name=group).exists()

class IsGroup(BasePermission):
    """Class that cheacks if a user belongs to a given group"""
    group_name: str

    @classmethod
    def check(cls, user: User) -> bool:
        return has_group(user, cls.group_name)
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        return (request.user.is_authenticated 
                and isinstance(request.user, User)
                and self.check(request.user))
    
class IsManager(IsGroup):
    group_name = 'Manager'

class IsAuthor(IsGroup):
    group_name = 'Author'

class IsModerator(IsGroup):
    group_name = 'Moderator'

class IsCustomer(IsGroup):
    """A customer is any authenticated user with no groups"""
    group_name = 'Customer' # unused variable as Customer isn't a real group, can be ignored

    @classmethod
    def check(cls, user: User) -> bool:
        return not user.groups.all().exists()

class PermissionCustomisationMixin:
    """Mixin that takes in a mapping of 'HTTP Method': PermissionClass and applies it in the get_permissions method"""
    permission_mapping: Mapping[str | tuple[str, ...], type[BasePermission]]

    @cached_property
    def permission_dict(self) -> dict[str, type[BasePermission]]:
        result: dict[str, type[BasePermission]] = {}
        for methods, permission_class in self.permission_mapping.items():
            if not isinstance(methods, tuple):
                methods = (methods,)
            for method in methods:
                result[method] = permission_class
        return result

    def get_permissions(self) -> Sequence[_SupportsHasPermission]:
        permission_class = self.permission_dict.get(self.request.method)  # type: ignore
        return [permission_class()] if permission_class is not None else []