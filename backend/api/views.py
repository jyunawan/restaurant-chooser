from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

User = get_user_model()


@method_decorator(csrf_protect, name="dispatch")
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            isAuthenticated = User.is_authenticated

            if isAuthenticated:
                return Response({"isAuthenticated": "success"})
            else:
                return Response({"isAuthenticated": "error"})
        except:
            return Response(
                {"error": "Something went wrong when checking authentication status"}
            )


@method_decorator(csrf_protect, name="dispatch")
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = self.request.data

        display_name = data["username"]
        email = data["email"]
        password = data["password"]
        re_password = data["re_password"]

        try:
            if password == re_password:

                if User.objects.filter(email=email).exists():
                    return Response({"error": "Email already exists"})

                else:
                    if len(password) < 8:
                        return Response(
                            {"error": "Passwords must be at least 8 characters"}
                        )
                    else:
                        user = User.objects.create_user(
                            email=email, password=password, display_name=display_name
                        )
                        user.save()

                        return Response({"success": "User created successfully"})

            else:
                return Response({"error": "Passwords do not match"})
        except:
            return Response({"error": "Something went wrong when registering accounts"})


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        email = data["email"]
        password = data["password"]

        try:
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({"success": "User authenticated", "email": email})
            else:
                return Response({"error": "Error Authenticating"})
        except:
            return Response({"error": "Something went wrong when logging in"})


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({"success": "Logged out"})
        except:
            return Response({"error": "Something went wrong when logging out"})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({"success": "CSRF cookie set"})
