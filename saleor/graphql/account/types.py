import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from graphene import relay

from ..core.types import CountableDjangoObjectType, PermissionDisplay
from ..utils import format_permissions_for_display

class User(CountableDjangoObjectType):
    permissions = graphene.List(PermissionDisplay)

    class Meta:
        exclude_fields = [
            'addresses', 'is_staff', 'is_active', 'date_joined', 'password',
            'default_shipping_address', 'default_billing_address',
            'is_superuser', 'last_login', 'ordernote_set',
            'orderhistoryentry_set']
        description = 'Represents user data.'
        interfaces = [relay.Node]
        model = get_user_model()

    def resolve_permissions(self, info, **kwargs):
        if self.is_superuser:
            permissions = Permission.objects.all()
        else:
            permissions = (
                self.user_permissions.all() |
                Permission.objects.filter(group__user=self))
        permissions = permissions.select_related('content_type')
        return format_permissions_for_display(permissions)
