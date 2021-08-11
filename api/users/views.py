
import os
import json
import json as simplejson
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
# from commons.utils.api_response import ApiResponse
from app.middlewares import login_exempt
from users.models import CustomUser as Users
from django.utils.timezone import now

# Create your views here.


class UnsafeSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, "user", None)

        if not user or not user.is_active:
            return None

        return (user, None)

class Account(APIView):
    """Account authentication"""

    auth_required=True if os.environ.get("IS_AUTHENTICATION_REQUIRED") == "True" else False
    authentication_classes = (UnsafeSessionAuthentication,)
    @staticmethod
    def parse_user(user):
        """Parses user details"""
        user_dict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "isSuperuser": user.is_superuser,
        }
        return user_dict

    def get(self, request):
        """Checks existing session, etc"""
        print("request", request)
        if self.auth_required:
            if request.user.is_authenticated and self.auth_required:
                user = Account.parse_user(request.user)
                Users.objects.filter(pk=request.user.pk)
                return Response({"data": user, "success": True, "isAuthenticationRequired": self.auth_required})
            else:
                # the login is a  GET request, so just show the user the login form.
                return Response({"message": "Please log in", "success": False, "isAuthenticationRequired": self.auth_required }, status=401)
        else:
                return Response({"message": "Authentication not required", "success": True, "isAuthenticationRequired": self.auth_required})




    def post(self, request):
            """For new login"""
            res = {"message": "Some error occured", "success": False}
            if request.method == "POST":
                body = json.loads(request.body)
                email = body["email"]
                password = body["password"]
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.status == "Active":
                        login(request, user)
                        res = {"message": "Logged in successfully", "success": True}
                    else:
                        # Return a 'disabled account' error message
                        res = {"message": "Account inactive, please contact administrator", "success": False}
                else:
                    # Return an 'invalid login' error message.
                    res = {"message": "Invalid login credentials", "success": False}
            # the login is a  GET request, so just show the user the login form.
            return Response(res)

    def delete(self, request):
        """Remove session, log outs user"""
        logout(request)
        return Response({"message": "Logged out successfully", "success":True})
