from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    @login_required(login_url='admin_panel:login')
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('landing')
        return view_func(request, *args, **kwargs)
    return wrapper
