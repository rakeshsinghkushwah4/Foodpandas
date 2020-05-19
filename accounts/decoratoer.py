from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(req,*args,**kwargs):
        if req.user.is_authenticated:
            return redirect('product')
        else:
            return view_func(req,*args,**kwargs)
    return wrapper_func

# this decorator is dynamic decorator
def  allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(req, *args, **kwargs):
            group =None
            if req.user.groups.exists():
                group=req.user.groups.all()[0].name
                if group in allowed_roles:
                    return view_func(req, *args, **kwargs)
                else:
                    return HttpResponse('You are note authorized to access this page')
        return wrapper_func
    return decorator


def seller_only(url):
    def decorator(view_func):
        def wrapper_func(req, *args, **kwargs):
            group = None
            if req.user.groups.exists():
                print('group')
                group = req.user.groups.all()[0].name
                print(group)
            if group=='customer':
                return redirect(url)
            if group=='seller' or group == 'admin':
                return view_func(req, *args, **kwargs)
        return wrapper_func
    return decorator

