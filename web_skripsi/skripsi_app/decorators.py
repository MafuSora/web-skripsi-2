from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request,*args, **kwargs):
            group_name = request.user.groups.values_list('name',flat = True)[0]
            if group_name in allowed_roles:
                return func(request,*args, **kwargs)
            else :
                raise PermissionDenied
        return wrap
    return decorator