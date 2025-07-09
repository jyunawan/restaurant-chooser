from django.urls import path
from .views import RegisterView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("csrf_cookie", GetCSRFToken.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("authenticated", CheckAuthenticatedView.as_view()),
]