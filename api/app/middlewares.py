from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.decorators import login_required

class DisableCsrfCheck(MiddlewareMixin):
    """
    Middleware class to disable CSRF check for views
    """

    def process_request(self, req):
        """
        Process request method to add attr _dont_enforce_csrf_checks
        """
        attr = "_dont_enforce_csrf_checks"
        if not getattr(req, attr, False):
            setattr(req, attr, True)


class LoginRequiredMiddleware:
    """
    Middleware class to enforce login for every view
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):  # pylint: disable=C0103
        """
        Process view method to check login_exempt decorator and enforce authentication on all views
        """
        try:
            appName = request.path.split("/")[1]
            if appName in ["admin", "accounts"]:
                return
        except:
            pass
        authenticationRequired= True if settings.AUTHENTICATION_REQUIRED == "True" else False
        if not authenticationRequired:
            return 
        if getattr(view_func, "login_exempt", False):
            return

        if not request.user.is_authenticated and request.path.split("/")[2] == "datadownload":
            return redirect(settings.LOGIN_REDIRECT_URL)

        if request.user.is_authenticated:
            if request.user.status != "Active":
                logout(request)
            return

        return login_required(view_func)(request, *view_args, **view_kwargs)




def login_exempt(view):  # pylint: disable=C0103
    """
    Decorator for views which needs to be exempted from login
    """
    view.login_exempt = True
    return view
