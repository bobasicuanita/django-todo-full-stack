from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.CreateUserView.as_view(), name="signup-form"),
    path("login/", views.LoginView.as_view(), name="login-form"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"),
    path("user/activate/<str:token>/", views.ActivateUserView.as_view(), name="activate_user"),
    path("user/password-reset/<str:token>/", views.ResetPasswordView.as_view(), name="reset-password"),
]
