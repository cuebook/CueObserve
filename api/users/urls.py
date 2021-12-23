from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from app.middlewares import login_exempt
from users import views
# from . import views

urlpatterns = [
    path("login/", login_exempt(csrf_exempt(views.Account.as_view())), name="login"),
    path("account/login/", login_exempt(csrf_exempt(views.Account.as_view())), name="login"),
    
    # Auth
    path("auth", views.AuthView.as_view(), name="auth"),

]